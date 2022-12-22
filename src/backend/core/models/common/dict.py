
class Dict:

    def __init__(self, _dict = None):
        self.dict = {}
        if _dict != None:
            self.dict.update(_dict)
    
    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        return 0

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __len__(self):
        return len(self.dict)
    
    def __iter__(self):
        return self.dict.__iter__()
