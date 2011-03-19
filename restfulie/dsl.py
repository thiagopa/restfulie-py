from processor import RedirectProcessor, PayloadMarshallingProcessor, \
    ExecuteRequestProcessor
from request import Request


class Dsl(object):
    """
    Configuration object for requests at a given URI.
    """

    HTTP_VERBS = ['delete', 'get', 'head', 'options', 'patch', 'post', 'put',
                  'trace']

    def __init__(self, uri):
        """
        Initialize the configuration for requests at the given URI.
        """
        self.credentials = self._parse_simple_auth(uri)
        self.uri = uri
        if self.credentials:
            self.uri = self._remove_auth_from_uri(self.uri)
        self.processors = [RedirectProcessor(),
                           PayloadMarshallingProcessor(),
                           ExecuteRequestProcessor(), ]
        self.headers = {'Content-Type': 'application/xml',
                        'Accept': 'application/xml'}
        self.is_async = False
        self.callback = None
        self.callback_args = ()

    def _parse_simple_auth(self, uri):
        if '@' in uri:
            protocol_and_auth, location = uri.split('@')
            protocol, user_and_pass = protocol_and_auth.split('//')
            return user_and_pass
        return None

    def _remove_auth_from_uri(self, uri):
        protocol_and_location = uri.split(self.credentials + '@')
        return ''.join(protocol_and_location)

    def __getattr__(self, name):
        """
        Perform an HTTP request. This method supports calls to the following
        methods: delete, get, head, options, patch, post, put, trace

        Once the HTTP call is performed, a response is returned (unless the
        async method is used).
        """
        if (self._is_verb(name)):
            self.verb = name.upper()
            return Request(self)
        else:
            raise AttributeError(name)

    def _is_verb(self, name):
        return name in self.HTTP_VERBS

    def use(self, feature):
        """
        Register a feature at this configuration.
        """
        self.processors.insert(0, feature)
        return self

    def async(self, callback=None, args=()):
        """
        Use asynchronous calls. A HTTP call performed through this object will
        return immediately, giving None as response. Once the request is
        completed, the callback function is called and the response and the
        optional extra args defined in args are passed as parameters.
        """
        self.is_async = True
        self.callback = callback
        self.callback_args = args
        return self

    def as_(self, content_type):
        if content_type:
            self.headers["Content-Type"] = content_type
        return self

    def accepts(self, content_type):
        """
        Configure the accepted response format.
        """
        self.headers['Accept'] = content_type
        return self
