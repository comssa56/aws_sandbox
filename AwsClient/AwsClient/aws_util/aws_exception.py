
class AwsException(Exception):
    pass

class APICallException(AwsException):
    pass

class InvalidValueException(AwsException):
    pass

class NotFoundException(AwsException):
    pass


