from typing import List, Optional
from .aws_ec2 import AwsEc2Object

class AwsEc2SecurityGroup(AwsEc2Object):    
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


    def __init__(self, data):
        super().__init__(data)

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



