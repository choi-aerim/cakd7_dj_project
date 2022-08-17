from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment


# 포스트 모델 등록
admin.site.register(Post, MarkdownxModelAdmin)

# 카테고리 모델 등록
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug' : ('name',)}
admin.site.register(Category, CategoryAdmin)

# 태그 모델 등록
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug' : ('name',)}
admin.site.register(Tag, TagAdmin)

#댓글 모델 등록
admin.site.register(Comment)

