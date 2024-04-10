from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    def __str__(self):
        return self.username
    
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    # content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_post', default=0)
    is_blog_post = models.BooleanField()

    def __str__(self):
        return self.title + ' | ' + str(self.author) 

    def get_absolute_url(self):
        return reverse('index')
    
    def total_likes(self):
        return self.likes.count()

    
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=800)
    date = models.DateTimeField()
    likes = models.IntegerField()
    posts_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    
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
    
class Population(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.CharField(max_length=50)
    population_2023 = models.IntegerField()
    population_2022 = models.IntegerField()
    population_2020 = models.IntegerField()
    population_2015 = models.IntegerField()
    population_2000 = models.IntegerField()