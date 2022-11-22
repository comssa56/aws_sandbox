
class AwsEc2Object(object):
    def __init__(self, data):
        self._data = data

    def is_valid(self) -> bool:
        return self._data is not None

    def name(self) -> str:
        return self.tag('Name')

    def tag(self, key) -> str:
        tags = self._data.get('Tags')
        if tags is not None:
            for v in tags:
                if v.get('Key')==key:
                    return v.get('Value')
            return None 


