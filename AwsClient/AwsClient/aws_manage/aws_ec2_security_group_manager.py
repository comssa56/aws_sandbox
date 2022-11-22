from typing import List

from aws_util.aws_client import AwsEc2Client
from aws_util.aws_ec2_security_group import AwsEc2SecurityGroup
from aws_util.aws_exception import APICallException
from aws_util.aws_response import AwsResponse


class AwsEc2SecurityGroupManager(object):

    ##########################
    # for Public
    ##########################
    @classmethod
    def fetch_by_group_names(cls, names :List[str]):
        client = AwsEc2Client()
        res = client.describe_security_groups_by_group_name(names)
        return cls.response2instances(res)

    @classmethod
    def fetch_by_names(cls, names :List[str]):
        client = AwsEc2Client()
        res = client.describe_security_groups_by_names(names)
        return cls.response2instances(res)

    @classmethod
    def fetch_by_name(cls, name :str):
        client = AwsEc2Client()
        res = client.describe_security_group_by_name(name)
        instances = cls.response2instances(res)
        return  instances[0] if len(instances)>0 else AwsEc2SecurityGroup(None)


    ##########################
    # for Private
    ##########################
    @classmethod
    def response2instances(cls, res :AwsResponse):
        if not res.is_http_success():
            raise APICallException( { "cls": cls.__name__, "func": sys._getframe().f_code.co_name })
        instances = res._data.get('SecurityGroups')
        return [AwsEc2SecurityGroup(i) for i in instances]




