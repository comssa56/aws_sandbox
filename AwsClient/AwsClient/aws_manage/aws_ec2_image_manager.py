from aws_util.aws_ec2 import AwsEc2Instance, AwsEc2Image
from aws_util.aws_exception import *

from typing import List

class AwsEc2ImageManager(object):
    @classmethod
    def fetch_images(cls) -> List[AwsEc2Image]:
        return AwsEc2Image.fetch()

    @classmethod
    def fetch_image_by_id(cls, id :str) -> AwsEc2Image:
        images = cls.fetch_images_by_ids([id])
        return images[0] if len(images)>0 else AwsEc2Image()

    @classmethod
    def fetch_images_by_ids(cls, ids :List[str]) -> List[AwsEc2Image]:
        return AwsEc2Image.fetch_by_ids(ids)

    @classmethod
    def fetch_image_by_name(cls, name :str) -> List[AwsEc2Image]:
        images = cls.fetch_images_by_names([name])
        return images[0] if len(images)>0 else AwsEc2Image()

    @classmethod
    def fetch_images_by_names(cls, names :List[str]) -> List[AwsEc2Image]:
        return AwsEc2Image.fetch_by_names(names)


    @classmethod
    def verify_for_create_image_from_instance(cls, name :str, instance_name :str) -> bool:
        base_instance = AwsEc2Instance.fetch_by_name(instance_name)
        image = cls.fetch_image_by_name(name)
        if image.is_valid():
            raise InvalidValueException(name)
        if not base_instance.is_valid():
            raise InvalidValueException(base_instance.instance_id())
        return True

    @classmethod
    def create_image_from_instnace(cls, name :str, instance_name :str) -> AwsEc2Image.ImageId:
        cls.verify_for_create_image_from_instance(name, instance_name)
        base_instance = AwsEc2Instance.fetch_by_name(instance_name)
        return AwsEc2Image.create_image_from_instance(name, base_instance)

    @classmethod
    def wait_create_image(cls, image_id :str):
        AwsEc2Image.wait_create_image(image_id)
