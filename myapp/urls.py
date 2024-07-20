from django.urls import path
from .views import login_page,register_page,dashboard,logout_page,create_blog_post,view_blog_posts

urlpatterns = [
    path('login/',login_page,name='login_page'),
    path('',register_page,name='register_page'),
    path('logout/',logout_page,name='logout_page'),
    path('dashboard/',dashboard,name='dashboard'),
    path('create-blog/',create_blog_post,name='create_blog_post'),
    path('blogs/',view_blog_posts,name='view_blog_posts'),
]