from restfulie.resources import Resource
from restfulie.links import Links, Link

class JsonResource(Resource):
    """
    This resource is returned when a JSON is unmarshalled.
    """

    def __init__(self, dict_):
        """
        JsonResource attributes can be accessed with 'dot'.
        """
        self._dict = dict_

        for key, value in dict_.items():
            if isinstance(value, (list, tuple)):
                d = [JsonResource(x) if isinstance(x, dict) else x for x in value]
                setattr(self, key, d)
            else:
                d = JsonResource(value) if isinstance(value, dict) else value
                setattr(self, key, d)

    def _find_dicts_in_dict(self, structure):
        """
        Get all dictionaries on a structure and returns a list of it.
        """
        dicts = []
        if isinstance(structure, dict):
            dicts.append(structure)
            for k, v in structure.items():
                dicts.extend(self._find_dicts_in_dict(v))
        return dicts

    def __len__(self):
        return len(self._dict)        
