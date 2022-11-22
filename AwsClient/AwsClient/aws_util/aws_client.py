from .aws_conf import AwsConf
from .aws_response import AwsResponse
import boto3
from typing import List, Dict

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

    '''
       ec2 instance
    '''
    def describe_instances(self, filters :List[Dict]) -> AwsResponse:
        return AwsResponse(self.connection().describe_instances(Filters=filters))

    def describe_instances_by_names(self, names :List[str]) -> AwsResponse:
        return self.describe_instances([{'Name':'tag:Name', 'Values':names}])

    def describe_instance_by_name(self, name :str) -> AwsResponse:
        return self.describe_instances_by_names([name])



    '''
       ec2 security group
    '''
    def describe_security_groups(self, filters) -> AwsResponse:
        return AwsResponse(self.connection().describe_security_groups(Filters=filters))

    def describe_security_groups_by_names(self, names :List[str]) -> AwsResponse:
        return self.describe_security_groups([{'Name':'tag:Name', 'Values':names}])

    def describe_security_group_by_name(self, name :str) -> AwsResponse:
        return self.describe_security_groups_by_names([name])


    '''
       ec2 image (AMI)
    '''
    def describe_images(self, image_ids, filters) -> AwsResponse:
        return AwsResponse(self.connection().describe_images(Owners=['self'], ImageIds=image_ids, Filters=filters))

    def describe_images_by_ids(self, ids :List[str]) -> AwsResponse:
        return self.describe_images(image_ids=ids, filters=[])

    def describe_images_by_names(self, names :List[str]) -> AwsResponse:
        return self.describe_images(image_ids=[], filters=[{'Name':'tag:Name', 'Values':names}])

    def modify_network_interface_attribute(self, dry_run :bool, network_interface_id : str, groups :List[str]) -> AwsResponse:
        return AwsResponse(self.connection().modify_network_interface_attribute(
            DryRun=dry_run,
            Groups=groups,
            NetworkInterfaceId=network_interface_id,
        ))

    def create_image(self, dry_run :bool, name :str, base_instance_id :str, description=''):
        return AwsResponse(self.connection().create_image(
            DryRun= dry_run,
            Name=name,
            InstanceId=base_instance_id,
            Description= description,
            NoReboot=False,
            TagSpecifications=[
                {
                    'ResourceType': 'image',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name
                        },
                    ]
                },
            ]))

    def get_waiter(self, waiter_name :str):
        return self.connection().get_waiter(waiter_name)
