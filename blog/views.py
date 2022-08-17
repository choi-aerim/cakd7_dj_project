from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

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
# createview 상속받고, 새 포스트 기재시 작성 내용을 field에 지정
# loginrequiredmixin: 로그인했을 때만 정상적으로 페이지가 보이게 됨
# UserPassesTestMixin: 사용자의 등급을 부여하고 특정 사용자만 포스트 작성 페이지 접근이 가능하도록 지정할 수 있음
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text','content','head_image','file_upload','category','tags']

    #지정 사용자인지, superuser인지 확인
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


    # author 필드를 자동으로 채우기 위해 CreateView의 form_valid() 함수 활용
    ## form_valid()함수는 방문자가 폼에 담아 보낸 유효한 정보를 사용해 포스트를 만들고, 포스트의 고유 경로로 보내주는 역할을 함
    def form_vaild(self,form):
        # self.request.user: 웹사이트 방문자
        current_user = self.request.user      
        #is_authenticated:현재 방문자가 로그인한 상태인지 확인
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user    #form에서 생성한 instance(새로생성포스트)의 author필드에 current_user을 담아라
            
            #태그와 관련된 작업 하기 전에 createview의 form_valid() 함수의 결과값을 resposne에 임시로 담아둠
            response = super(PostCreate, self).form_valid(form)

            #장고가 작성한 post_html폼은 method가 post임. 추가된 input 값(새로운 태그)은 post방식으로 postcreate까지 전달되며, 그 값을 가져오도록 함
            tags_str = self.request.POST.get('tags_str')

            #값이 빈칸인 경우
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    # tag: tag모델의 인스턴스, is_tag_created: 인스턴스가 생성되었는지 bool 값
                    # t를 name으로 갖는 태그가 있다면 가져오고, 없다면, 새로 만들기
                    tag, is_tag_created = Tag.objects.get_or_create(name = t) 
                    #생성되었다면 slug 값 생성, 한글 ㅇㅋ
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode = True)
                        tag.save()
                    #새로만든 태그나 기존 태그 모두 새로 만든 포스트의tag 필드에 추가해야함
                    #self.object : 이번에 새로만든 태그
                    self.object.tags.add(tag)

            return response

        else:
            return redirect('/blog/')     #로그인하지 않은 상태면 /blog/ 경로로 돌려보냄


    

# CBV 방식으로 포스트를 수정할 수 있도록 PostUpdate 클래스 생성
# 이미 수정하려는 포스트에 작성자가 존재하므로 form_valid()함수 사용 안함
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category','tags']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        return context

    #dispatch(): 방문자가 웹사이트 서버에 get방식으로 요청했는지 post 방식으로 요청했는지 판단
    ## get: 포스트를 작성할 수 있는 폼 페이지 보내줌
    ## post: 같은 경로로 폼에 내용을 담아 post 방식으로 들어오면, 폼이 유효한지 확인하고 문제없으면 db에 저장
    def dispatch(self, request, *args, **kwargs):
        # 포스트의 작성자와 로그인한 유저와 동일할 시, dispatch()함수 작용
        # self.get_object(): updateview의 메서드로 Post.objects.get(pk = pk)와 동일한 역할
        if request.user.is_authenticated and request.user == self.get_object().author:  
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied    #조건 불만족 시, 권한 없음을 나타냄

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
    
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',',';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name = t)
                if is_tag_created:
                    tag.slug = slugify(t,allow_unicode = True)
                    tag.save()
                self.object.tags.add(tag)
        return response



    

    
    

