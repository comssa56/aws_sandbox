from .aws_conf import AwsConf
from .aws_response import AwsResponse
import boto3


class AwsInstance():
    _data = None

    def __init__(self, data):
        self._data = data


class AwsClient(object):
    _connection = None

    def __init__(self, resource_name :str):
        conf = AwsConf()
        access_conf = conf.get(conf.KEY_ACCESS)
        self._connection = boto3.client(
            resource_name,
            region_name=access_conf.get(conf.KEY_ACCESS_REGION, ""),
            aws_access_key_id=access_conf.get(conf.KEY_ACCESS_TOKEN, ""),
            aws_secret_access_key=access_conf.get(conf.KEY_ACCESS_SECRET, "")
            )

    def connection(self):
        return self._connection



class AwsEc2Client(AwsClient):
    def __init__(self):
        super().__init__("ec2")

    def describe_instance_by_name(self, name):
        return AwsResponse(self.connection().describe_instances(Filters=[{'Name':'tag:Name', 'Values':[name]}]))

    def describe_instances_by_name(self, names):
        return AwsResponse(self.connection().describe_instances(Filters=[{'Name':'tag:Name', 'Values':names}]))

    def describe_security_group_by_name(self, name):
        return AwsResponse(self.connection().describe_security_groups(Filters=[{'Name':'tag:Name', 'Values':[name]}]))

    def describe_security_groups_by_name(self, names):
        return AwsResponse(self.connection().describe_security_groups(Filters=[{'Name':'tag:Name', 'Values':names}]))
