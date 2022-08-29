from aws_util.aws_ec2 import *
from aws_util.aws_exception import *

from typing import List

class AwsEc2SecurityGroupManager(object):
    @classmethod
    def fetch_security_groups_by_name(cls, names :List[str]) -> List[AwsEc2SecurityGroup]:
        return AwsEc2SecurityGroup.fetch_by_names(names)

    @classmethod
    def fetch_security_group_by_name(cls, name :str) -> AwsEc2SecurityGroup
        return AwsEc2SecurityGroup.fetch_by_name(name)


    @classmethod
    def verify_for_add_security_group_to_instance(cls, instance_name :str, sg_name :str) -> bool:
        instance = AwsEc2Instance.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroup.fetch_by_name(sg_name)
        if not instance.is_valid():
            raise NotFoundException(instance_name)
        if not sg.is_valid():
            raise NotFoundException(sg_name)
        return True

    @classmethod
    def add_security_group_to_instance(cls, instance_name :str, sg_name :str, dry_run :bool = False)->bool:
        cls.verify_for_add_security_group_to_instance(instance_name, sg_name)
        instance = AwsEc2Instance.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroup.fetch_by_name(sg_name)
        sgs = instance.security_groups()
        sgs.append(sg)
        return AwsEc2Util.modify_network_interface_attribute(dry_run, instance, sgs)

    @classmethod
    def verify_for_delete_security_group_to_instance(cls, instance_name :str, sg_name :str) -> bool:
        instance = AwsEc2Instance.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroup.fetch_by_name(sg_name)
        if not instance.is_valid():
            raise NotFoundException(instance_name)
        if not sg.is_valid():
            raise NotFoundException(sg_name)
        return True

    @classmethod
    def delete_security_group_to_instance(cls, instance_name :str, sg_name :str, dry_run :bool = False)->bool:
        cls.verify_for_delete_security_group_to_instance(instance_name, sg_name)
        instance = AwsEc2Instance.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroup.fetch_by_name(sg_name)
        sgs = list(filter(lambda _sg: _sg.group_id()!=sg.group_id(), instance.security_groups()))
        return AwsEc2Util.modify_network_interface_attribute(dry_run, instance, sgs)


