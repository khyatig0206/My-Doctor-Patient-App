from django.contrib.auth.models import AbstractUser
from django.db import models
from mediSys import settings
from django.utils import timezone
class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/',default='profile-default.png')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()

    def __str__(self) -> str:
        return self.user.email
    

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='blog_images/',null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True) 
    summary = models.TextField(max_length=500,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments')
    speciality = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = (timezone.datetime.combine(timezone.now(), self.start_time) + timezone.timedelta(minutes=45)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.get_full_name()} on {self.date} at {self.start_time}"