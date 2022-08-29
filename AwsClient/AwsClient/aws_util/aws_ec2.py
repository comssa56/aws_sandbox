from .aws_client import AwsEc2Client
from .aws_exception import APICallException, InvalidValueException

from typing import List, Optional
import sys

class AwsEc2Object(object):
    def __init__(self, data):
        self._data = data

    def is_valid(self) -> bool:
        return self._data is not None

    def name(self) -> str:
        return self.tag('Name')

    def tag(self, key) -> str:
        tags = self._data.get('Tags')
        if tags is not None:
            for v in tags:
                if v.get('Key')==key:
                    return v.get('Value')
            return None 


class AwsEc2Instance(AwsEc2Object):
    class NetworkInterface:
        def __init__(self, network_interface):
            self._data = network_interface

        def id(self) -> str:
            return self._data.get('NetworkInterfaceId')

    class State:
        def __init__(self, state):
            self._data = state

        def code(self):
            return self._data.get('code')

        def name(self):
            return self._data.get('Name')

    class SecurityGroup:
        def __init__(self, sg):
            self._data = sg

        def group_id(self):
            return self._data.get('GroupId')

        def group_name(self):
            return self._data.get('GroupName')

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
        return  instances[0] if len(instances)>0 else AwsEc2Instance(None)

    def __init__(self, data):
        super().__init__(data)

    def is_valid(self) -> bool:
        return super().is_valid() and self.instance_id() != ""

    def instance_id(self) -> Optional[str]:
        return self._data.get('InstanceId')

    def vpc_id(self) -> Optional[str]:
        return self._data.get('VpcId')

    def instance_type(self) -> Optional[str]:
        return self._data.get('InstanceType')

    def public_ip(self) -> Optional[str]:
        return self._data.get('PublicIpAddress')

    def state(self) -> State:
        return self.State(self._data.get('State'))

    def security_groups(self) -> List[SecurityGroup]:
        return [ self.SecurityGroup(sg) for sg in self._data.get('SecurityGroups')]

    def network_interfaces(self) -> List[NetworkInterface]:
        return [ self.NetworkInterface(ni) for ni in self._data.get('NetworkInterfaces') ]

    def describe(self) -> str:
        text = ""
        text += f"InstanceName  : {self.name()}\n"    
        text += f"InstanceId    : {self.instance_id()}\n"    
        text += f"InstanceType  : {self.instance_type()}\n"    
        text += f"PublicIP      : {self.public_ip()}\n"    
        text += f"State         : {self.state().name()}\n"    
        text += f"SecurityGroups: {[ sg.group_name() for sg in self.security_groups() ]}\n"    
        return text

    ##########################
    # for Private
    ##########################
    @classmethod
    def response2instances(cls, res):
        if not res.is_http_success():
            raise APICallException( { "cls": cls.__name__} )

        reservations = res._data.get('Reservations')
        if len(reservations)==0:
            return None

        instances = reservations[0].get('Instances')
        return [AwsEc2Instance(i) for i in instances]


class AwsEc2SecurityGroup(AwsEc2Object):    
    ##########################
    # for Public
    ##########################
    SECURITY_GROUP_MAX = 5
    class IpPermission:
        class IpRange:
            def __init__(self, range):
                self._data = range

            def cidr_ip(self) -> str:
                return self._data.get('CidrIp')

        def __init__(self, permission):
            self._data = permission

        def from_port(self)->str:
            return self._data.get('FromPort')

        def ip_protocol(self)->str:
            return self._data.get('IpProtocol')

        def ip_ranges(self)->str:
            return [ self.IpRange(ip) for ip in self._data.get("IpRanges", [])  ]


    @classmethod
    def fetch_by_group_names(cls, names :List[str]):
        client = AwsEc2Client()
        res = client.describe_security_groups_by_group_name(names)
        return cls.response2instances(res)

    @classmethod
    def fetch_by_names(cls, names :List[str]):
        client = AwsEc2Client()
        res = client.describe_security_groups_by_name(names)
        return cls.response2instances(res)

    @classmethod
    def fetch_by_name(cls, name :str):
        client = AwsEc2Client()
        res = client.describe_security_group_by_name(name)
        instances = cls.response2instances(res)
        return  instances[0] if len(instances)>0 else AwsEc2SecurityGroup(None)

    def is_valid(self) -> bool:
        return super().is_valid() and self.group_id() != None

    def group_id(self) -> Optional[str]:
        return self._data.get('GroupId')

    def group_name(self) -> Optional[str]:
        return self._data.get('GroupName')

    def ip_permissions(self) -> List[IpPermission]:
        return [ self.IpPermission(ipp) for ipp in self._data.get("IpPermissions", [])  ]
    
    def describe(self) -> str:
        text = ""
        text += f"GroupName     : {self.group_name()}\n"    
        text += f"GroupId       : {self.group_id()}\n"    
        text += f"Name          : {self.name()}\n"    

        for ipp in self.ip_permissions():
            text += f"IP FROM PORT: { ipp.from_port() }\n"  
            text += f"IP PROTOCOL : { ipp.ip_protocol() }\n"  
            text += f"IP RANGES   : { [ ip.cidr_ip() for ip in ipp.ip_ranges() ]}\n"  

        return text

    ##########################
    # for Private
    ##########################
    @classmethod
    def response2instances(cls, res):
        if not res.is_http_success():
            raise APICallException( { "cls": cls.__name__, "func": sys._getframe().f_code.co_name })
        instances = res._data.get('SecurityGroups')
        return [AwsEc2SecurityGroup(i) for i in instances]

    def __init__(self, data):
        super().__init__(data)


class AwsEc2Image(AwsEc2Object):
    ImageId = str

    ##########################
    # for Public
    ##########################
    @classmethod
    def fetch(cls):
        client = AwsEc2Client()
        res = client.describe_images()
        return cls.response2instances(res)

    @classmethod
    def fetch_by_ids(cls, ids :List[str]):
        client = AwsEc2Client()
        res = client.describe_images_by_ids(ids)
        return cls.response2instances(res)

    @classmethod
    def fetch_by_names(cls, names :List[str]):
        client = AwsEc2Client()
        res = client.describe_images_by_names(names)
        return cls.response2instances(res)

    @classmethod
    def create_image_from_instance(cls, name :str, base_instance: AwsEc2Instance) -> str:
        client = AwsEc2Client()
        res = client.create_image(False, name, base_instance.instance_id())
        if not res.is_http_success():
            raise APICallException( { "cls": cls.__name__, "func": sys._getframe().f_code.co_name })
        return res._data.get('ImageId')

    @classmethod
    def wait_create_image(cls, image_id :str):
        waiter = cls.get_waiter_for_image_available()
        waiter.wait(
            ImageIds=[image_id],
            Owners=['self'],
            IncludeDeprecated=False,
            DryRun=False,
            WaiterConfig={
                'Delay': 15,
                'MaxAttempts': 40
            }
        )

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


    ##########################
    # for Private
    ##########################
    @classmethod
    def response2instances(cls, res) -> List['AwsEc2Image']:
        if not res.is_http_success():
            raise APICallException( { "cls": cls.__name__, "func": sys._getframe().f_code.co_name })
        instances = res._data.get('Images')
        return [AwsEc2Image(i) for i in instances]

    @classmethod
    def get_waiter_for_image_available(cls):
        client = AwsEc2Client()
        return client.get_waiter('image_available')

    def __init__(self, data=None):
        super().__init__(data)




class AwsEc2Util:

    @classmethod
    def modify_network_interface_attribute(cls, dry_run :bool, instance :AwsEc2Instance, security_groups :List[AwsEc2SecurityGroup])->bool:
        if not instance.is_valid():
            raise InvalidValueException()    
        ###############################
        # This validation is hoped, but this security_groups is expected from AwsEc2Instance, that do not have enough param for AwsEc2SecurityGroup.
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
        

