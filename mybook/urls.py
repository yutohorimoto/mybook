from django.urls import path
from django.contrib.auth import login, logout
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    #path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    #path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    #url(r'^logout/$', logout, {'template_name': 'templates/mybook/login.html'}, name='logout'), 
    #url(r'^create/$', views.create_account, name='create_account'),
    #url(r'^login/$', views.account_login, name='login'),
    #ath(r'logout/', logout, {'template_name': 'login.html'}, name='logout'), 
    path(r'create/', views.create_account, name='create_account'),
    path(r'login/', views.account_login, name='login'),
    #path(r'logout/',views.Account_logout, name='logout'), 
    #path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("logout/",views.MyLogoutView.as_view(template_name='mybook/logout.html'),name="logout"),
    #path('mypage/',views.MyPage.as_view(template_name='mybook/mypage.html'),name ='mypage')
    path('mypage/',views.MyPageView.as_view(),name ='mypage'),
    path('accounts/login/',views.account_login, name='account_login'),
    #path('follow/<int:pk>/', views.followPost, name='follow'),
    path('post/<int:pk>/like', views.like, name='like'),
]