from django.db import models

# Create your models here.
# class Member(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=50)
#     username = models.CharField(max_length=30)
#     email = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)
    
# class Posts(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     member = models.CharField()
#     content = models.CharField()
#     date = models.DateTimeField()
#     likes = models.IntegerField()
#     is_blog_post = models.BooleanField()
    
# class Comments(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     content = models.CharField()
#     date = models.DateTimeField()
#     likes = models.IntegerField()
#     posts_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    
