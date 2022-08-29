from aws_util.aws_ec2 import AwsEc2Instance, AwsEc2Image
from aws_util.aws_exception import *

from typing import Iterable, Iterator, List

class AwsEc2ImageManager(object):
    @classmethod
    def fetch_images(cls) -> List[AwsEc2Image]:
        return AwsEc2Image.fetch()

    @classmethod
    def fetch_images_by_name(cls, name :str) -> List[AwsEc2Image]:
        images = cls.fetch_images_by_names([name])
        return images[0] if len(images)>0 else AwsEc2Image()

    @classmethod
    def fetch_images_by_names(cls, names :List[str]) -> List[AwsEc2Image]:
        return AwsEc2Image.fetch_by_names(names)

    @classmethod
    def create_image_from_instnace(cls, name :str, base_instance :AwsEc2Instance):
        image = cls.fetch_images_by_name(name)
        if image.is_valid():
            raise InvalidValueException(name)
        if not base_instance.is_valid():
            raise InvalidValueException(base_instance.instance_id())

        return AwsEc2Image.create_image_from_instance(name, base_instance)

