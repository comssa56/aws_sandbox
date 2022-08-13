
class AwsResponse(object):
    _data = None
    def __init__(self, response):
        self._data = response

    def get_meta(self):
        return ResponseMetaData(self._data)

    def is_http_success(self):
        meta = self.get_meta()
        return meta.is_valid() and meta.is_success()

class ResponseMetaData(object):
    _data = None
    def __init__(self, response):
        self._data = response.get('ResponseMetadata')

    def is_valid(self):
        return self._data is not None

    def is_success(self):
        return self._data.get('HTTPStatusCode') == 200
