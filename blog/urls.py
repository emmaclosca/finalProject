from django.urls import path
from . import views
from .views import IndexView, BlogView, AddPost, UpdatePost, DeletePost

urlpatterns = [
    # path("", views.index, name="index"),
    path('index/', IndexView.as_view(), name="index"),
    path('blog/<int:pk>/', BlogView.as_view(), name='blogContent'),
    path('addPost/', AddPost.as_view(), name="addPost"),
    path('blog/update/<int:pk>', UpdatePost.as_view(), name="updatePost"),
    path('blog/<int:pk>/delete', DeletePost.as_view(), name="deletePost"),
    path("signUp/", views.signUp, name="signUp"),
    path("logIn/", views.logIn, name="logIn"),
    path("guest/", views.guest, name="guest"),
    path("news/", views.news, name="news"),
    path("forum/", views.forum, name="forum"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("russia/", views.russia, name="russia"),
    path("palestine/", views.palestine, name="palestine"),
    path("zimbabwe/", views.zimbabwe, name="zimbabwe"),   
]
