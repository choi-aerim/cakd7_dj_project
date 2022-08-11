from xml.etree.ElementInclude import include
from django.urls import path
from . import views


urlpatterns = [
    # Python/만 떼어 views.py의 tag_page 함수로 보냄
    path('tag/<str:slug>/', views.tag_page),
    
    # 사용자가 127.0.0.1:8000/blog/category/Python/을 입력하면, 
    # Python/만 떼어 views.py의 category_page 함수로 보냄
    path('category/<str:slug>/', views.category_page),

    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),

    

]

