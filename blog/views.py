from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Category, Tag

# ListView를 상속받은 PostList 클래스 생성
# model = Post 선언 시, get_context_data에서 자동으로 post_list = Post.objects.all()을 명령함
#  ==> 따라서 html파일에서 for문에 post_list를 사용할 수 있는 것
class PostList(ListView):
    model =  Post
    ordering = 'pk'

    #get_context_data 오버라이딩 
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()   # 기존의 get_context_data() 내용 그대로 저장
        
        #원하는 쿼리셋을 만들어 딕셔너리형태로 context에 담기
        context['categories'] = Category.objects.all()    #모든 카테고리 소환
        context['no_category_post_count'] = Post.objects.filter(category=None).count()   #카테고리가 미분류된 개수 세기

        return context



# DetailView를 상속받은 PostDetail 클래스 생성
class PostDetail(DetailView):
    model =  Post

    #get_context_data 오버라이딩 
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()   # 기존의 get_context_data() 내용 그대로 저장
        
        #원하는 쿼리셋을 만들어 딕셔너리형태로 context에 담기
        context['categories'] = Category.objects.all()    #모든 카테고리 소환
        context['no_category_post_count'] = Post.objects.filter(category=None).count()   #카테고리가 미분류된 개수 세기

        return context

# FBV 방식으로 카테고리 함수 추가
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category = None)
    else:
        category = Category.objects.get(slug = slug)
        post_list = Post.objects.filter(category = category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category = None).count(),
            'category': category,
        }
    )
    
# FBV 방식으로 태그 함수 추가
def tag_page(request, slug):
    tag = Tag.objects.get(slug = slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag': tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category = None).count(),
        }
    )


# CBV 방식으로 포스트 생성 가능하도록 CreateView 클래스 추가
class PostCreate(CreateView):
    model = Post,
    fields = ['title', 'hook_text','content','head_image','file_upload','category']



