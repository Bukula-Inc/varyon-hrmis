class Dict_To_Object(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update((key, Dict_To_Object(value) if isinstance(value, dict) else self._convert_list(value) if isinstance(value, list) else value) for key, value in self.items())
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def _convert_list(self, value):
        return [Dict_To_Object(item) if isinstance(item, dict) else item for item in value]
    


class Object_To_Dict:
    def __init__(self, obj):
        self.obj = obj

    def to_dict(self):
        return self._convert(self.obj)

    def _convert(self, obj):
        if isinstance(obj, dict):
            return self._convert_dict(obj)
        elif isinstance(obj, list):
            return self._convert_list(obj)
        else:
            return self._convert_object(obj)

    def _convert_dict(self, dictionary):
        return {key: self._convert(value) for key, value in dictionary.items()}

    def _convert_list(self, lst):
        return [self._convert(item) for item in lst]

    def _convert_object(self, obj):
        if hasattr(obj, '__dict__'):
            return self._convert_dict(obj.__dict__)
        else:
            return obj
