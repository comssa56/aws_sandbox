from aws_util.aws_ec2 import *
from aws_util.aws_exception import *

from typing import List

class AwsEc2InstanceManager(object):

    @classmethod
    def fetch_instance_by_names(cls, names :List[str]) -> List[AwsEc2Instance]:
        return AwsEc2Instance.fetch_by_names(names)
    
    @classmethod
    def fetch_instance_by_name(cls, name :str) -> AwsEc2Instance:
        return AwsEc2Instance.fetch_by_name(name)





