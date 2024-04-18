from django import forms
from .models import Post, Comment, Category


choices = Category.objects.all().values_list('name', 'name')

category_list = []

for item in choices:
    category_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "is_blog_post"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(choices=category_list, attrs={'class': 'form-control'}),
            "is_blog_post": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }
