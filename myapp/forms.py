from django import forms
from .models import BlogPost,Appointment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a brief summary'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your content here'}),
            
        }
    

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['speciality', 'date', 'start_time']
        widgets = {
            'speciality':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter required Speciality'}),
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control','type': 'time'}),
        }