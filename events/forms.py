from django import forms
from django.contrib.auth.models import User
from .models import Event  ,BookingEvent

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name']




class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer',]
        #fields = '__all__'

class BookingEventForm(forms.ModelForm):
    class Meta:
        model = BookingEvent
        exclude = ['user',]
        #fields = '__all__'




#class DashboardForm(forms.ModelForm):
#    class Meta:
#        model = Dashboard
#        fields = '__all__'
