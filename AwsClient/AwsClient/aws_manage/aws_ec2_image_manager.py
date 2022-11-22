from typing import List
from aws_util.aws_client import AwsEc2Client
from aws_util.aws_ec2_image import AwsEc2Image
from aws_util.aws_exception import APICallException, InvalidValueException
from aws_util.aws_response import AwsResponse

class AwsEc2ImageManager(object):
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
    def fetch_by_name(cls, name :str):
        images = cls.fetch_by_names([name])
        return images[0] if len(images)>0 else AwsEc2Image(None)

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

    ##########################
    # for Private
    ##########################
    @classmethod
    def response2instances(cls, res :AwsResponse) -> List['AwsEc2Image']:
        if not res.is_http_success():
            raise APICallException({ "cls": cls.__name__, "func": sys._getframe().f_code.co_name })
        instances = res._data.get('Images')
        return [AwsEc2Image(i) for i in instances]

    @classmethod
    def get_waiter_for_image_available(cls):
        client = AwsEc2Client()
        return client.get_waiter('image_available')


