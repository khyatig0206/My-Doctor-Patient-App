from django.urls import path
from .views import login_page,register_page,dashboard,logout_page,create_blog_post,view_blog_posts,doctors_view,book_appointment,appointment_confirm,oauth_callback,view_appointments

urlpatterns = [
    path('login/',login_page,name='login_page'),
    path('',register_page,name='register_page'),
    path('logout/',logout_page,name='logout_page'),
    path('dashboard/',dashboard,name='dashboard'),
    path('create-blog/',create_blog_post,name='create_blog_post'),
    path('blogs/',view_blog_posts,name='view_blog_posts'),
    path('doctors/',doctors_view,name='doctors_view'),
    path('doctors/book_appointment/<int:doctor_id>',book_appointment,name='book_appointment'),

    path('appointment/confirm/<int:appointment_id>/', appointment_confirm, name='appointment_confirm'),

    path('oauth2callback/', oauth_callback, name='oauth_callback'),

    path('appointments/', view_appointments, name='view_appointments'),
]