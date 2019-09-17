import random
import time
from hashlib import sha1

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from qcloud_cos import CosConfig, CosS3Client

secret_id = settings.COS_SECRET_ID
secret_key = settings.COS_SECRET_KEY
region = settings.REGION
bucket = settings.BUCKET
config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key)
client = CosS3Client(config)
host = 'https://' + bucket + '.cos.' + region + '.myqcloud.com/'


@deconstructible
class CosStorage(Storage):

    def save(self, name, content, max_length=None):
        """
        我没有实现_save()方法，而是直接重写了save()方法，因为save()其实是调用了_save()方法，
        所以这样简单粗暴，不知有没有坑。
        """
        suffix = name.split('.')[-1]
        key = self.generate_key(suffix)
        try:
            response = client.put_object(
                Bucket=bucket,
                Body=content.read(),
                Key=key,
                EnableMD5=False
            )
        except Exception as e:
            raise
        return host + key

    def generate_key(self, suffix):
        """
          给文件重命名
        """
        file_name = str(int(time.time() * 10000000)) + ''.join([str(random.randint(1, 9)) for i in range(3)])
        s = sha1()
        s.update(file_name.encode('utf-8'))
        file_name = str(s.hexdigest())
        key = file_name + '.' + suffix
        return key

    def url(self, name):
        return name