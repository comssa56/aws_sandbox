from aws_util.aws_ec2 import *
from aws_util.aws_exception import *

class AwsEc2Manager(object):

    @classmethod
    def fetch_instance_by_names(cls, names :List[str]) -> List[AwsEc2Instance]:
        return AwsEc2Instance.fetch_by_names(name)
    
    @classmethod
    def fetch_instance_by_name(cls, name :str) -> AwsEc2Instance:
        return AwsEc2Instance.fetch_by_name(name)

    @classmethod
    def fetch_security_groups_by_name(cls, names :List[str]) -> List[AwsEc2Instance]:
        return AwsEc2SecurityGroup.fetch_by_names(names)

    @classmethod
    def fetch_security_group_by_name(cls, name :str) -> AwsEc2Instance:
        return AwsEc2SecurityGroup.fetch_by_name(name)

    @classmethod
    def add_security_group_to_instance(cls, instance_name :str, sg_name :str)->bool:
        instance = AwsEc2Instance.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroup.fetch_by_name(sg_name)
        if not instance.is_valid() or not sg.is_valid():
            return False

        sgs = instance.security_groups()
        sgs.append(sg)
        return AwsEc2Util.modify_network_interface_attribute(False, instance, sgs)

    @classmethod
    def delete_security_group_to_instance(cls, instance_name :str, sg_name :str)->bool:
        instance = AwsEc2Instance.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroup.fetch_by_name(sg_name)
        if not instance.is_valid() or not sg.is_valid():
            return False

        sgs = list(filter(lambda _sg: _sg.group_id()!=sg.group_id(), instance.security_groups()))
        return AwsEc2Util.modify_network_interface_attribute(False, instance, sgs)

