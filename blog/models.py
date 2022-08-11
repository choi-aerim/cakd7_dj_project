from django.db import models
import os

# foreign 키로 author 필드 구현하기
from django.contrib.auth.models import User


# tag 구현하기
class Tag(models.Model):
    name = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'blog/tag/{self.slug}'


# category 구현하기
class Category(models.Model):
    # unique=True: 동일한 이름 사용 금지
    # SlugField: 사람이 읽을 수 있는 텍스트로 고유 url 만들기
    # allow_unicode = True: 한글로 만들 수 있도록 함
    name = models.CharField(max_length = 50, unique = True)
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'    

    class Meta:
        verbose_name_plural = 'Categories'

# blog post 구현하기
class Post(models.Model):
    title =  models.CharField(max_length = 30)
    hook_text = models.CharField(max_length=100, blank = True)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    head_image = models.ImageField(upload_to = 'blog/images/%Y/%m/%d/', blank = True)    
    file_upload = models.FileField(upload_to = 'blog/files/%Y/%m/%d/', blank = True)

    # foreign 키로 author 필드 구현하기
    # on_delete = models.CASCADE: 이 포스트의 작성자가 데이터베이스에서 삭제될 경우, 이 포스트도 삭제하겠단 의미
    # null = True: 카테고리가 미분류인 포스트도 있을 수 있도록 함(이전에 포스팅했던 것들)
    # blank = True: 카테고리 필수입력 요소가 아님
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)

    category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL)

    tags = models.ManyToManyField(Tag, null = True, blank = True)
    
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]






    
