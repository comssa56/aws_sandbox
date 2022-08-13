from typing import Any, Dict, Optional

class AwsConf(object):

    KEY_ACCESS = "access"
    KEY_ACCESS_PROJECT = "project"
    KEY_ACCESS_REGION = "region"
    KEY_ACCESS_TOKEN = "token"
    KEY_ACCESS_SECRET = "secret"

    KEY_PROFILE = "profile" 
    KEY_PROFILE_OWNER = "owner" 
    
    KEY_EC2 = "ec2"
    KEY_EC2_NAME = "name"
    KEY_EC2_INSTANCE_ID = "instance_id"

    CONF = {
        KEY_ACCESS : {
            KEY_ACCESS_REGION : "",
            KEY_ACCESS_TOKEN  : "",
            KEY_ACCESS_SECRET : ""
            },
        KEY_PROFILE : {
            KEY_PROFILE_OWNER : "980159776202"
            },
        KEY_EC2 : [
            {
                KEY_EC2_NAME : "",
                KEY_EC2_INSTANCE_ID : "",
            },
            ]
        }

    @classmethod
    def get_conf_org(cls) -> Dict[str, Any]:
        return cls.CONF

    def __init__(self):
        self.conf = self.get_conf_org()

    def get(self, key :str) -> Optional[Any]:
        return self.conf.get(key, None)

