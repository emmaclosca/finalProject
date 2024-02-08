from django.db import models

# Create your models here.
class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
class Posts(models.Model):
    id = models.BigAutoField(primary_key=True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField()
    likes = models.IntegerField()
    is_blog_post = models.BooleanField()
    
class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=800)
    date = models.DateTimeField()
    likes = models.IntegerField()
    posts_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    
class Content(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2000)
    publish_date = models.DateTimeField()
    author = models.CharField(max_length=80)
    publisher = models.CharField(max_length=80)
    country = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    description = models.TextField()
    image_url = models.CharField(max_length=2000)
    video_url = models.CharField(max_length=2000)
    
