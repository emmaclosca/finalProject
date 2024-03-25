from django.contrib import admin
from .models import Post, Member

admin.site.register(Member)
admin.site.register(Post)