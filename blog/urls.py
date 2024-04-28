from django.urls import path
from . import views
from .views import (
    AddForumPost, DeleteForumPost, EditProfile, ForumDetail, ForumView, 
    IndexView, BlogView, AddPost, UpdateForumPost, UpdatePost, DeletePost, 
    LikeView, AddComment
)

urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    path("homepage/", views.homepage, name="homepage"),
    # Blog URLs
    path("blog/<int:pk>/", BlogView.as_view(), name="blogContent"), 
    path("addPost/", AddPost.as_view(), name="addPost"),
    path("blog/update/<int:pk>/", UpdatePost.as_view(), name="updatePost"),
    path("blog/<int:pk>/delete/", DeletePost.as_view(), name="deletePost"),
    # Forum URLs
    path("forum/", ForumView.as_view(), name="forum"),
    path("forum/<int:pk>/", ForumDetail.as_view(), name="forumDetail"),
    path("forum/addPost/", AddForumPost.as_view(), name="addForumPost"),
    path("forum/update/<int:pk>/", UpdateForumPost.as_view(), name="updateForumPost"),
    path("forum/<int:pk>/delete/", DeleteForumPost.as_view(), name="deleteForumPost"),
    # User authentication URLs
    path("signUp/", views.signUp, name="signUp"),
    path("logIn/", views.logIn, name="logIn"),
    path("guest/", views.guest, name="guest"),
    # News URLs
    path("news/", views.news, name="news"),
    path("russia/", views.russia, name="russia"),
    path("palestine/", views.palestine, name="palestine"),
    path("zimbabwe/", views.zimbabwe, name="zimbabwe"),
    # Like and comment URLs 
      path("like/<int:pk>", LikeView, name="likePosts"),
    path("blog/<int:pk>/addComment/", AddComment.as_view(), name="addComment"),
    # Profile and settings URLs
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("editProfile/", EditProfile.as_view(), name="editProfile"),
    # Category URLs
    path("general/", views.GeneralView.as_view(), name="general"),
    path("educational/", views.EducationalView.as_view(), name="educational"),
]
