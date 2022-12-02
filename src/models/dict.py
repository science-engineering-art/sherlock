

class Dict:

    def __new__(cls, _dict = None):
        result = object.__new__(cls)
        if _dict:
            result.__dict__.update(_dict)
        return result
    
    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return 0

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __len__(self):
        return len(self.__dict__)
    
    def __iter__(self):
        return self.__dict__.__iter__()