from django.db import models
# foreign 키로 author 필드 구현하기
from django.contrib.auth.models import User
# 마크다운된 필드 보여주는 것 구현하기 
from markdownx.models import MarkdownxField
# 마크다운된 필드를 html파일로 수정해서 구현하기
from markdownx.utils import markdown
import os

# tag 구현하기
class Tag(models.Model):
    name = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'


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

    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    head_image = models.ImageField(upload_to = 'blog/images/%Y/%m/%d/', blank = True)    
    file_upload = models.FileField(upload_to = 'blog/files/%Y/%m/%d/', blank = True)

    # foreign 키로 author 필드 구현하기
    # on_delete = models.CASCADE: 이 포스트의 작성자가 데이터베이스에서 삭제될 경우, 이 포스트도 삭제하겠단 의미
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    
    # null = True: 카테고리가 미분류인 포스트도 있을 수 있도록 함(이전에 포스팅했던 것들)
    # blank = True: 카테고리 필수입력 요소가 아님
    category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank = True)
    
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    # content 텍스트를 마크다운 적용된 html파일로 변경
    def get_content_markdown(self):
        return markdown(self.content)


# 댓글창 달기
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add = True)
    modified_at = models.DateField(auto_now = True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        # #이 HTML 요소의 id를 의미함
        # 웹브라우저가 해당 포스트의 페이지를 열고 comment -{self.pk}에 해당하는 위치로 이동함
        return f'{self.post.get_absolute_url()}#comment - {self.pk}'

    
