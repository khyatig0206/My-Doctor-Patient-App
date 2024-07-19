from django.urls import path
from .views import login_page,register_page,dashboard,logout_page

urlpatterns = [
    path('login/',login_page,name='login_page'),
    path('register/',register_page,name='register_page'),
    path('logout/',logout_page,name='logout_page'),
    path('dashboard/',dashboard,name='dashboard')
]