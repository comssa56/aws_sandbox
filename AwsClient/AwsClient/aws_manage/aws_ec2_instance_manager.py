from typing import List

from aws_util.aws_client import AwsEc2Client
from aws_util.aws_ec2_instance import AwsEc2Instance
from aws_util.aws_exception import APICallException
from aws_util.aws_response import AwsResponse


class AwsEc2InstanceManager(object):

    ##########################
    # for Public
    ##########################
    @classmethod
    def fetch(cls):
        client = AwsEc2Client()
        res = client.describe_instances(filters=None)
        return cls.response2instances(res)

    @classmethod
    def fetch_by_names(cls, names :List[str]):
        client = AwsEc2Client()
        res = client.describe_instances_by_name(names)
        return cls.response2instances(res)

    @classmethod
    def fetch_by_name(cls, name :str):
        client = AwsEc2Client()
        res = client.describe_instance_by_name(name)
        instances = cls.response2instances(res)
        return  instances[0] if instances is not None and len(instances)>0 else AwsEc2Instance(None)

    
    ##########################
    # for Private
    ##########################
    @classmethod
    def response2instances(cls, res :AwsResponse):
        if not res.is_http_success():
            raise APICallException( { "cls": cls.__name__} )

        reservations = res._data.get('Reservations')
        if len(reservations)==0:
            return None

        ret = []
        for reservation in reservations:
            instances = reservation.get('Instances')
            ret.extend([AwsEc2Instance(i) for i in instances])
        return ret

