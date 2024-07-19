from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile,CustomUser
from django.contrib.auth import authenticate, login, logout
import time
# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return HttpResponseRedirect(request.path_info)
    
    return render(request, 'account/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        select_role = request.POST.get('select_role')
        profile_picture = request.FILES.get('profile_picture', 'profile-default.png')

        if password == confirm_password:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            if select_role == 'patient':
                user.is_patient = True
            elif select_role == 'doctor':
                user.is_doctor = True
            user.save()  

            profile = Profile.objects.create(user=user, address=address, state=state, pincode=pincode, city=city, profile_picture=profile_picture)
            profile.save()

            messages.success(request, "Registration successful.")
            return redirect('login_page')  
        else:
            messages.warning(request, "Passwords do not match.")
            return HttpResponseRedirect(request.path_info)

    return render(request, 'account/register.html')


def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    user=request.user
    return render(request, 'account/dashboard.html',context={'user':user,'profile':profile})


def logout_page(request):
    logout(request)
    return redirect('login_page')