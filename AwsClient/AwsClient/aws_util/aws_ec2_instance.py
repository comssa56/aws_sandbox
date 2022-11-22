from typing import List, Optional
from .aws_ec2 import AwsEc2Object


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

    def security_groups(self) -> List['SecurityGroup']:
        return [ self.SecurityGroup(sg) for sg in self._data.get('SecurityGroups')]

    def network_interfaces(self) -> List['NetworkInterface']:
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


