from django.contrib import admin
from .models import Post, Member, Comment

admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Comment)