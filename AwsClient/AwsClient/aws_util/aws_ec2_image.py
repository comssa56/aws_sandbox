from typing import Optional
from .aws_ec2 import AwsEc2Object

class AwsEc2Image(AwsEc2Object):
    Available = 'available'
    Pending = 'pending'
    Failed = 'failed'

    def __init__(self, data=None):
        super().__init__(data)

    def is_valid(self) -> bool:
        return super().is_valid() and self.image_id() != None

    def image_id(self)->Optional[str]:
        return self._data.get('ImageId')

    def image_name(self)->Optional[str]:
        return self._data.get('Name')

    def state(self)->Optional[str]:
        return self._data.get('State')

    def describe(self)->str:
        text = ""
        text += f"Name          : {self.name()}\n"    
        text += f"ImageName     : {self.image_name()}\n"    
        text += f"ImageId       : {self.image_id()}\n"    
        text += f"State         : {self.state()}\n"    
        return text



