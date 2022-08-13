
from aws_manage.aws_ec2 import AwsEc2Manager

sgs = AwsEc2Manager.fetch_security_groups_by_name(['tk', 'test-sg', 'test-sg2'])

AwsEc2Manager.add_security_group_to_instance('test', 'test-sg2')
instance = AwsEc2Manager.fetch_instance_by_name('test')
print(instance.describe())
AwsEc2Manager.delete_security_group_to_instance('test', 'test-sg2')
instance = AwsEc2Manager.fetch_instance_by_name('test')
print(instance.describe())

