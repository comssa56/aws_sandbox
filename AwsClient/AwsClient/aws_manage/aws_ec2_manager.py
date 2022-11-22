from typing import List
from aws_manage.aws_ec2_image_manager import AwsEc2ImageManager
from aws_manage.aws_ec2_instance_manager import AwsEc2InstanceManager
from aws_manage.aws_ec2_security_group_manager import AwsEc2SecurityGroupManager
from aws_util.aws_client import AwsEc2Client
from aws_util.aws_ec2_instance import AwsEc2Instance
from aws_util.aws_ec2_security_group import AwsEc2SecurityGroup
from aws_util.aws_exception import InvalidValueException, NotFoundException


class AwsEc2Manager(object):
    ##########################
    # for Public
    ##########################

    #
    # Add/Del Security Group
    @classmethod
    def verify_for_add_security_group_to_instance(cls, instance_name :str, sg_name :str) -> bool:
        instance = AwsEc2InstanceManager.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroupManager.fetch_by_name(sg_name)
        if not instance.is_valid():
            raise NotFoundException(instance_name)
        if not sg.is_valid():
            raise NotFoundException(sg_name)
        return True

    @classmethod
    def add_security_group_to_instance(cls, instance_name :str, sg_name :str, dry_run :bool = False)->bool:
        cls.verify_for_add_security_group_to_instance(instance_name, sg_name)
        instance = AwsEc2InstanceManager.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroupManager.fetch_by_name(sg_name)
        sgs = instance.security_groups()
        sgs.append(sg)
        return cls.modify_network_interface_attribute(dry_run, instance, sgs)

    @classmethod
    def verify_for_delete_security_group_to_instance(cls, instance_name :str, sg_name :str) -> bool:
        instance = AwsEc2InstanceManager.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroupManager.fetch_by_name(sg_name)
        if not instance.is_valid():
            raise NotFoundException(instance_name)
        if not sg.is_valid():
            raise NotFoundException(sg_name)
        return True

    @classmethod
    def delete_security_group_to_instance(cls, instance_name :str, sg_name :str, dry_run :bool = False)->bool:
        cls.verify_for_delete_security_group_to_instance(instance_name, sg_name)
        instance = AwsEc2InstanceManager.fetch_by_name(instance_name)
        sg = AwsEc2SecurityGroupManager.fetch_by_name(sg_name)
        sgs = list(filter(lambda _sg: _sg.group_id()!=sg.group_id(), instance.security_groups()))
        return cls.modify_network_interface_attribute(dry_run, instance, sgs)


    #
    # Create Image
    @classmethod
    def verify_for_create_image_from_instance(cls, image_name :str, instance_name :str) -> bool:
        base_instance = AwsEc2InstanceManager.fetch_by_name(instance_name)
        image = AwsEc2ImageManager.fetch_by_name(image_name)
        if image.is_valid():
            raise InvalidValueException(image_name)
        if not base_instance.is_valid():
            raise InvalidValueException(instance_name)
        return True

    @classmethod
    def create_image_from_instance(cls, image_name :str, instance_name :str) -> str:
        cls.verify_for_create_image_from_instance(image_name, instance_name)
        base_instance = AwsEc2InstanceManager.fetch_by_name(instance_name)

        client = AwsEc2Client()
        res = client.create_image(False, image_name, base_instance.instance_id())
        if not res.is_http_success():
            raise APICallException( { "cls": cls.__name__, "func": sys._getframe().f_code.co_name })

        return res._data.get('ImageId')

    ##########################
    # for Private
    ##########################
    @classmethod
    def modify_network_interface_attribute(cls, dry_run :bool, instance :AwsEc2Instance, security_groups :List[AwsEc2SecurityGroup])->bool:
        if not instance.is_valid():
            raise InvalidValueException()    
        ###############################
        # This validation is hoped, but this security_groups is expected from AwsEc2Instance, that do not have enough param for verify AwsEc2SecurityGroup.
        ###############################
        #for sg in security_groups:
        #    if not sg.is_valid():
        #        raise InvalidValueException()
        if len(security_groups) > AwsEc2SecurityGroup.SECURITY_GROUP_MAX:
                raise InvalidValueException()

        client = AwsEc2Client()
        res = client.modify_network_interface_attribute(dry_run, instance.network_interfaces()[0].id(),
                                                        [sg.group_id() for sg in security_groups])
        return res.is_http_success()
        



