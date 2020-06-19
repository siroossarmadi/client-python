class Key:
    def __init__(self, type_: str, name: str, namespace: str):
        self.Type = type_
        self.Name = name
        self.Namespace = namespace

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['Type'], data['Name'], data['Namespace'])


class Object:
    def __init__(self, key: Key, value=''):
        self.Key = key
        self.Value = value
        self.Meta = ''

    @classmethod
    def from_dict(cls, data: dict):
        return cls(Key.from_dict(data['Key']), data['Value'])
