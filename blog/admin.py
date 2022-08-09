from django.contrib import admin
from .models import Post, Category

# 포스트 모델 등록
admin.site.register(Post)

# 카테고리 모델 등록
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)