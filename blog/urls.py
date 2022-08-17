from xml.etree.ElementInclude import include
from django.urls import path
from . import views


urlpatterns = [

    path('', views.PostList.as_view()),
    
    path('<int:pk>/', views.PostDetail.as_view()),
    
    # 사용자가 127.0.0.1:8000/blog/category/Python/을 입력하면, 
    # Python/만 떼어 views.py의 category_page 함수로 보냄
    path('category/<str:slug>/', views.category_page),
    
    # Python/만 떼어 views.py의 tag_page 함수로 보냄
    path('tag/<str:slug>/', views.tag_page),

    # 새 포스트 생성시, creat_post 클래스로 보냄
    path('create_post/', views.PostCreate.as_view()),

    # 포스트 수정
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),

    # 댓글
    path('<int:pk>/new_comment/', views.new_comment),

    # 댓글 수정
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
]

