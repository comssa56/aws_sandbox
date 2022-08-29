
from aws_manage.aws_ec2_security_group_manager import AwsEc2SecurityGroupManager
from aws_manage.aws_ec2_instance_manager import AwsEc2InstanceManager
from aws_manage.aws_ec2_image_manager import AwsEc2ImageManager

#AwsEc2SecurityGroupManager.add_security_group_to_instance('test', 'test-sg2')
#instance = AwsEc2InstanceManager.fetch_instance_by_name('test')
#print(instance.describe())

#AwsEc2SecurityGroupManager.delete_security_group_to_instance('test', 'test-sg2')
#instance = AwsEc2InstanceManager.fetch_instance_by_name('test')
#print(instance.describe())

image_id = AwsEc2ImageManager.create_image_from_instnace( 'test11-image',  'test')
AwsEc2ImageManager.wait_create_image(image_id)
image = AwsEc2ImageManager.fetch_image_by_id(image_id)
print(image.describe())

images = AwsEc2ImageManager.fetch_images()
for image in images:
    print(image.describe())
