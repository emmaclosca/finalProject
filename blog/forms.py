from django import forms
from .models import Post, Comment, Category, User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


choices = Category.objects.all().values_list('name', 'name')

category_list = []

for item in choices:
    category_list.append(item)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "is_blog_post"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "is_blog_post": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ForumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ForumForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['is_blog_post'].initial = False  # Set default value to False
        self.fields['is_blog_post'].widget = forms.HiddenInput()  # Hide this field from the form

    class Meta:
        model = Post
        fields = ["title", "content", "category", "is_blog_post"]  
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
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


class EditProfileForm(UserChangeForm):
    password = None  # This line ensures the password field is not handled by this form
    
    class Meta:
        model = User
        fields = ("username", "email") 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

User = get_user_model()

class PasswordChangedForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'id': 'id_old_password'}))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'id': 'id_new_password1'}))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'id': 'id_new_password2'}))

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")

