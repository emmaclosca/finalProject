from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', views.signUp, name='signup'),
    path('login/', views.logIn, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logOut, name='logout'),
]
