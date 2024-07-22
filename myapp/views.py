from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Profile,CustomUser,BlogPost,Appointment
from django.contrib.auth import authenticate, login, logout
from .forms import BlogPostForm,AppointmentForm
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDS_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Check if the user has already authenticated with Google
            if not request.session.get('credentials'):
                # Redirect the user to the Google OAuth flow
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
                flow.redirect_uri = 'http://127.0.0.1:8000/oauth2callback'  # Update this to your actual redirect URI
                authorization_url, state = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true'
                )
                return redirect(authorization_url)
            
            return redirect('dashboard')
        else:
            messages.warning(request, "Invalid username or password.")
            return HttpResponseRedirect(request.path_info)
    
    return render(request, 'account/login.html')





def oauth_callback(request):
    flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/oauth2callback'  # This should match your redirect URI
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials
    request.session['credentials'] = creds.to_json()

    return redirect('dashboard')






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



def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  # Set the author field here
            if 'save_as_draft' in request.POST:
                blog_post.draft = True
            else:
                blog_post.draft = False
            blog_post.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_create.html', {'form': form})




def view_blog_posts(request):
    blog_posts = BlogPost.objects.filter(draft=False).order_by('created_at')
    user=request.user
    
    blog_drafts=BlogPost.objects.filter(draft=True,author=request.user).order_by('created_at')
    
    return render(request, 'blog/blog_view.html', {'blog_posts': blog_posts,'blog_drafts':blog_drafts})





def doctors_view(request):
    profiles = Profile.objects.filter(user__is_doctor=True)
    return render(request, 'doctor/doctors_view.html', {'profiles': profiles})






SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDS_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')


def create_google_calendar_event(request, appointment):
    # Get the credentials from the session
    credentials_info = request.session.get('credentials')
    if credentials_info:
        creds = Credentials.from_authorized_user_info(credentials_info)
    else:
        # Handle the case where credentials are not found
        raise Exception("User is not authenticated with Google.")

    service = build('calendar', 'v3', credentials=creds)

    start_datetime = datetime.datetime.combine(appointment.date, appointment.start_time)
    end_datetime = start_datetime + datetime.timedelta(minutes=45)

    event = {
        'summary': f'Appointment with Dr. {appointment.doctor.get_full_name()}',
        'description': appointment.speciality,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'IST',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'IST',
        },
        'attendees': [
            {'email': appointment.doctor.email},
        ],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event






def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Profile, id=doctor_id, user__is_doctor=True)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor.user
            appointment.save()
            event = create_google_calendar_event(appointment)
            appointment.google_event_id = event['id']
            appointment.save()
            return redirect('appointment_confirm', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'doctor/book_appointment.html', {'form': form, 'doctor': doctor})

def appointment_confirm(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'doctor/appointment_confirm.html', {'appointment': appointment})

def view_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'account/view_appointments.html', {'appointments': appointments})