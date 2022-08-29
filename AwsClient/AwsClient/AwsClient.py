
from aws_manage.aws_ec2 import AwsEc2Manager
from aws_manage.aws_ec2_image_manager import AwsEc2ImageManager

#AwsEc2Manager.add_security_group_to_instance('test', 'test-sg2')
#instance = AwsEc2Manager.fetch_instance_by_name('test')
#print(instance.describe())

#AwsEc2Manager.delete_security_group_to_instance('test', 'test-sg2')
#instance = AwsEc2Manager.fetch_instance_by_name('test')
#print(instance.describe())

#instance = AwsEc2Manager.fetch_instance_by_name('test')
#if instance.is_valid():
#    images = AwsEc2ImageManager.create_image_from_instnace( 'test2-image',  instance)

images = AwsEc2ImageManager.fetch_images()
for image in images:
    print(image.describe())
