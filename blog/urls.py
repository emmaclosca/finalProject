from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'), 
    path('signUp/', views.signUp, name= 'signUp'),
    path('logIn/', views.logIn, name= 'logIn'),
    path('news/', views.news, name= 'news'),
    path('forum/', views.forum, name= 'forum'),
    path('profile/', views.profile, name= 'profile'),
    path('settings/', views.settings, name= 'settings'),
    path('russia/', views.russia, name= 'russia'),
    path('palestine/', views.palestine, name= 'palestine'),
    path('zimbabwe/', views.zimbabwe, name= 'zimbabwe'),
]
