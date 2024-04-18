from django.contrib import admin
from .models import Post, Member, Comment, Category

admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)