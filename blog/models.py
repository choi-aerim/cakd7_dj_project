from django.db import models
import os

# foreign 키로 author 필드 구현하기
from django.contrib.auth.models import User



# Create your models here.

class Post(models.Model):
    title =  models.CharField(max_length = 30)
    hook_text = models.CharField(max_length=100, blank = True)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    head_image = models.ImageField(upload_to = 'blog/images/%Y/%m/%d/', blank = True)    
    file_upload = models.FileField(upload_to = 'blog/files/%Y/%m/%d/', blank = True)

    # foreign 키로 author 필드 구현하기
    # on_delete: 이 포스트의 작성자가 데이터베이스에서 삭제될 경우, 이 포스트도 삭제하겠단 의미
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

