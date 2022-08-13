
from aws_util import aws_client, aws_conf, aws_ec2

conf = aws_conf.AwsConf()
client = aws_client.AwsEc2Client()

ret = aws_ec2.AwsEc2Instance.fetch_by_name('test')
print(ret.instance_id())
print(ret.name())

ret = aws_ec2.AwsEc2SecurityGroup.fetch_by_name('tk')
print(ret.group_id())
print(ret.name())
