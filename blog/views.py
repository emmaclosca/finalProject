import base64
from io import BytesIO
from django.urls import reverse, reverse_lazy
import matplotlib

# import requests
from http.client import (
    REQUEST_ENTITY_TOO_LARGE,
    REQUEST_HEADER_FIELDS_TOO_LARGE,
    REQUEST_TIMEOUT,
)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
import matplotlib.pyplot as plt
from django.contrib import messages
from numpy import generic
from .decorators import unauthenticated_user, allowed_users
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Category, Member, Post, Comment
from django.utils import timezone
from .forms import BlogForm, EditProfileForm, UpdateForm, CommentForm, ForumForm, PasswordChangedForm

from . import models

matplotlib.use("agg")


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else: 
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('blogContent', args=[str(pk)]))


def index(request):
    if request.user.is_authenticated:
        username = (
            request.user.username
        )  # this takes the logged in username and used for the "Hello, username" in the navbar
        # print(request.user.groups)
        return render(
            request,
            "index.html",
            {"username": username},
        )
    else:
        return redirect("signUp")
    

# blog operations
class IndexView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = "blog_post"
    ordering = ["-id"]

    def get_queryset(self):
        return Post.objects.filter(is_blog_post=True).order_by('-id') # only shows the blog posts 


class BlogView(DetailView):
    model = Post
    template_name = "blogDetail.html"
    
    def get_context_data(self, *args, **kwargs):
        # Correctly call the super method to get the context.
        context = super(BlogView, self).get_context_data(*args, **kwargs)

        # Retrieve the post and calculate total likes.
        likes = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = likes.total_likes()  # Ensure this method returns the correct value
        liked = False
        if likes.likes.filter(id=self.request.user.id).exists():
            liked = True
        # Add total_likes to the context.
        context["total_likes"] = total_likes
        context["liked"] = liked

        return context


class AddPost(CreateView):
    model = Post
    form_class = BlogForm
    template_name = "addBlog.html"

    def form_valid(self, form):
        form.instance.date = timezone.now()
        form.instance.author = self.request.user  # Set the author directly to the current user
        return super().form_valid(form)


class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "addComment.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure the post is fetched using 'pk' from the URL
        context['post'] = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        post_pk = self.kwargs.get('pk')
        return reverse('blogContent', kwargs={'pk': post_pk})


class UpdatePost(UpdateView):
    model = Post
    template_name = "updateBlog.html"
    form_class = UpdateForm


class DeletePost(DeleteView):
    model = Post
    template_name = "deleteBlog.html"
    success_url = reverse_lazy("index")


# forum operations
class ForumView(ListView):
    model = Post
    template_name = "forum.html"
    context_object_name = "forum_post"
    ordering = ["-id"]

    def get_queryset(self):
        return Post.objects.filter(is_blog_post=False).order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch posts categorized as "General"
        general_category = Category.objects.get(name='General')
        general_posts = Post.objects.filter(category=general_category)
        
        # Fetch posts categorized as "Educational"
        educational_category = Category.objects.get(name='Educational')
        educational_posts = Post.objects.filter(category=educational_category)
        
        context["general_posts"] = general_posts
        context["educational_posts"] = educational_posts
        return context
    

class ForumDetail(DetailView):
    model = Post
    template_name = "forumDetail.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ForumDetail, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'], is_blog_post=False)
        total_likes = post.total_likes()
        liked = post.likes.filter(id=self.request.user.id).exists()
        context.update({
            "total_likes": total_likes,
            "liked": liked
        })
        return context
    

class AddForumPost(CreateView):
    model = Post
    form_class = ForumForm
    template_name = "addForum.html"

    def form_valid(self, form):
        form.instance.date = timezone.now()
        form.instance.author = self.request.user
        form.instance.is_blog_post = False  # Ensure this is a forum post
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum')
    

class UpdateForumPost(UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = "updateForum.html"

    def get_queryset(self):
        return Post.objects.filter(is_blog_post=False)
    
    def get_success_url(self):
        return reverse_lazy('forum')
    

class DeleteForumPost(DeleteView):
    model = Post
    template_name = "deleteForum.html"
    success_url = reverse_lazy("forum")


# categories
class GeneralView(ListView):
    model = Post
    template_name = "generalCat.html"
    context_object_name = "category_posts"

    def get_queryset(self):
        # Retrieve the General category
        general_category = Category.objects.get(name__iexact='General')
        # Fetch posts belonging to the General category
        return Post.objects.filter(category=general_category)


class EducationalView(ListView):
    model = Post
    template_name = "educationalCat.html"
    context_object_name = "category_posts"

    def get_queryset(self):
        # Retrieve the Educational category
        educational_category = Category.objects.get(name__iexact='Educational')
        # Fetch posts belonging to the Educational category
        return Post.objects.filter(category=educational_category)
   

# this @unauthenticated_user is being called from the decorators
@unauthenticated_user
def signUp(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        passwordConfirm = request.POST.get("passwordConfirm")

        if password != passwordConfirm:
            return HttpResponse("Your passwords do not match, try again.")
        else:
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            Member.objects.create(user=my_user, name=name, username=username, email=email, password=password)
            messages.success(request, "Your account was created successfully, " + username)
            return redirect("login")

    return render(request, "signUp.html", {})


@unauthenticated_user
def logIn(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Username or password is incorrect.")

    return render(request, "logIn.html", {})


def guest(request):
    user = authenticate(request, username="guest", password="passwordabc")
    login(request, user)

    return redirect("index")


# guest users are not allowed to view this page
@allowed_users(allowed_roles=["moderators", "members"])
def russia(request):
    data = {
        "2023": 144444359,
        "2022": 144713314,
        "2020": 145617329,
        "2015": 144668389,
        "2010": 143242599,
        "2000": 146844839,
    }
    names = list(data.keys())[::-1]
    values = list(data.values())[::-1]

    plt.figure()
    plt.plot(names, values, linestyle="dotted")

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
    buf.close()

    all_entries = models.Content.objects.filter(country="Russia")

    # Determine whether the user has access based on the decorator
    has_access = request.user.groups.filter(name__in=["moderators", "members"]).exists()

    return render(
        request,
        "russia.html",
        {
            "image_base64": image_base64,
            "content": all_entries,
            "has_access": has_access,
        },
    )


# guest users are not allowed to view this page
@allowed_users(allowed_roles=["moderators", "members"])
def palestine(request):
    # Determine whether the user has access based on the decorator
    has_access = request.user.groups.filter(name__in=["moderators", "members"]).exists()

    data = {
        "2023": 5371230,
        "2022": 5250072,
        "2020": 5019401,
        "2015": 4484614,
        "2010": 3992278,
        "2000": 3139954,
    }
    names = list(data.keys())[::-1]
    values = list(data.values())[::-1]

    plt.figure()
    plt.plot(names, values, linestyle="dotted")

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
    buf.close()

    all_entries = models.Content.objects.filter(country="Sri Lanka")
    return render(
        request,
        "palestine.html",
        {
            "image_base64": image_base64,
            "content": all_entries,
            "has_access": has_access,
        },
    )


# guest users are not allowed to view this page
@allowed_users(allowed_roles=["moderators", "members"])
def zimbabwe(request):
    # Determine whether the user has access based on the decorator
    has_access = request.user.groups.filter(name__in=["moderators", "members"]).exists()

    data = {
        "2023": 16665409,
        "2022": 16320537,
        "2020": 15669666,
        "2015": 14154937,
        "2010": 12839771,
        "2000": 11834676,
    }
    names = list(data.keys())[::-1]
    values = list(data.values())[::-1]

    plt.figure()
    plt.plot(names, values, linestyle="dotted")

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
    buf.close()

    all_entries = models.Content.objects.filter(country="Zimbabwe")
    return render(
        request,
        "zimbabwe.html",
        {
            "image_base64": image_base64,
            "content": all_entries,
            "has_access": has_access,
        },
    )


def news(request):
    return render(request, "news.html", {})


def profile(request):
    return render(request, "profile.html", {})


class EditProfile(UpdateView):
    form_class = EditProfileForm
    template_name = "editProfile.html"
    success_url = reverse_lazy("index")

    def get_object(self):
        return self.request.user
    

class ChangePassword(PasswordChangeView):
    form_class = PasswordChangedForm
    template_name = 'changePassword.html'  
    success_url = reverse_lazy('passwordSuccess') 


def passwordSuccess(request):
    return render(request, "passwordSuccess.html", {})


def settings(request):
    return render(request, "settings.html", {})


def logOut(request):
    logout(request)
    return redirect("logIn")


# def news(request):
#     api_url = 'https://api.api-ninjas.com/v1/country?name=Russia'
#     headers = {'X-Api-Key': 'ZLPOykr1PiSkaMTpZxUYPg==1qes8BJwWRpO0GQl'}

#     response = requests.get(api_url, headers=headers)

#     if response.status_code == requests.codes.ok:
#         data = response.json()
#         population = data[0]['population']
#         return render(request, 'news.html', {'population': population})
#     else:
#         return JsonResponse({'error': 'Failed to fetch data'}, status=500)
