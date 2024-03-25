from django.db import models
from django.urls import reverse
class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    def __str__(self):
        return self.username
    
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    is_blog_post = models.BooleanField()

    def __str__(self):
        return self.title + ' | ' + str(self.author) 

    def get_absolute_url(self):
        return reverse('index')

    
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