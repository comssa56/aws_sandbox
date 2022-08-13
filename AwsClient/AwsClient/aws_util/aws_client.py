from .aws_conf import AwsConf
from .aws_response import AwsResponse
import boto3
from typing import List

class AwsClient(object):
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

    def describe_instance_by_name(self, name) -> AwsResponse:
        return AwsResponse(self.connection().describe_instances(Filters=[{'Name':'tag:Name', 'Values':[name]}]))

    def describe_instances_by_name(self, names) -> AwsResponse:
        return AwsResponse(self.connection().describe_instances(Filters=[{'Name':'tag:Name', 'Values':names}]))

    def describe_security_group_by_name(self, name) -> AwsResponse:
        return AwsResponse(self.connection().describe_security_groups(Filters=[{'Name':'tag:Name', 'Values':[name]}]))

    def describe_security_groups_by_name(self, names) -> AwsResponse:
        return AwsResponse(self.connection().describe_security_groups(Filters=[{'Name':'tag:Name', 'Values':names}]))

    def describe_images(self) -> AwsResponse:
        return AwsResponse(self.connection().describe_images(Owners=['self']))

    def modify_network_interface_attribute(self, dry_run :bool, network_interface_id : str, groups :List[str]) -> AwsResponse:
        return AwsResponse(self.connection().modify_network_interface_attribute(
            DryRun=dry_run,
            Groups=groups,
            NetworkInterfaceId=network_interface_id,
        ))
