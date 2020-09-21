from django.urls import path
from django.contrib.auth import login, logout
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    #url(r'^logout/$', logout, {'template_name': 'templates/mybook/login.html'}, name='logout'), 
    #url(r'^create/$', views.create_account, name='create_account'),
    #url(r'^login/$', views.account_login, name='login'),
    #ath(r'logout/', logout, {'template_name': 'login.html'}, name='logout'), 
    path(r'create/', views.create_account, name='create_account'),
    path(r'login/', views.account_login, name='login'),
    path(r'logout/',logout,  name='logout'), 
]