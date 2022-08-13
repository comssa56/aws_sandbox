from .aws_client import AwsEc2Client, AwsInstance

class AwsEc2Object(object):
    _data = None

    def __init__(self, data):
        self._data = data

    def is_valid(self) -> bool:
        return self._data is not None

    def name(self) -> str:
        return self.tag('Name')

    def tag(self, key) -> str:
        tags = self._data.get('Tags')
        for v in tags:
            if v.get('Key')==key:
                return v.get('Value')
        return None 


class AwsEc2Instance(AwsEc2Object):

    @classmethod
    def fetch_by_names(cls, names):
        client = AwsEc2Client()
        res = client.describe_instances_by_name(names)

        if not res.is_http_success():
            return None

        reservations = res._data.get('Reservations')
        if len(reservations)==0:
            return None

        instances = reservations[0].get('Instances')
        return [AwsEc2Instance(i) for i in instances]

    @classmethod
    def fetch_by_name(cls, name :str) ->AwsEc2Instance:
        client = AwsEc2Client()
        res = client.describe_instance_by_name(name)
        
        if not res.is_http_success():
            return None

        reservations = res._data.get('Reservations')
        if len(reservations)==0:
            return None

        instances = reservations[0].get('Instances')
        assert len(instances)==1 
        return AwsEc2Instance(instances[0])


    def __init__(self, data):
        super().__init__(data)

    def is_valid(self) -> bool:
        return super().is_valid() and self.instance_id() != ""

    def instance_id(self) -> str:
        return self._data.get('InstanceId', "")


class AwsEc2SecurityGroup(AwsEc2Object):

    @classmethod
    def fetch_by_names(cls, names):
        client = AwsEc2Client()
        res = client.describe_security_groups_by_name

        if not res.is_http_success():
            return None

        instances = res._data.get('SecurityGroups')
        return [AwsEc2SecurityGroup(i) for i in instances]

    @classmethod
    def fetch_by_name(cls, name :str) ->AwsEc2SecurityGroup:
        client = AwsEc2Client()
        res = client.describe_security_group_by_name(name)
        
        if not res.is_http_success():
            return None

        groups = res._data.get('SecurityGroups')
        assert len(groups)==1 
        return AwsEc2SecurityGroup(groups[0])

    def __init__(self, data):
        super().__init__(data)

    def is_valid(self) -> bool:
        return super().is_valid() and self.group_id() != ""

    def group_id(self) -> str:
        return self._data.get('GroupId', "")
    