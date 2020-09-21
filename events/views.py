from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin ,EventForm
from django.contrib import messages
from .models import Event , Dashboard
from .permissions import owner
from datetime import date


def home(request):
	return render(request, 'home.html')

class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, "Welcome Back!")
				return redirect('dashboard')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")



#class Dashboard(View):
#    return redirect("dashboard")

#def Dashboard(request , user_id):
#	user = Dashboard.objects.get(id=user_id)
#	if  not request.user==user.owner:
#		eventupcoming=Event.objects.filter(date_event__gt=date.today())
		#event = Event.objects.all()
#		context = {
				#"events": event,
#				"eventupcoming":eventupcoming,
#			}
#		return render(request, 'dashboard.html', context)


def Dashboard(request):
	if  request.user.is_staff:
		event= Event.objects.all()
	else:
		event=Event.objects.filter(date_event__gt=date.today())
	#event = Event.objects.all()
	#owner =event.organizer.owner
	context = {
			"events": event,
			#"eventupcoming":eventupcoming,
		}
	return render(request, 'dashboard.html', context)

def event_create(request):


		form = EventForm()
		if request.method == "POST":
			form = EventForm(request.POST )
			if form.is_valid():
				#event=form.save(commit=False)
				#event.organizer=request.user
				form.save()
				messages.success(request, ' add  success.')
				return redirect('dashboard')
			#else:
			#    messages.success(request, ' not  success.')
		context = {
				"form":form,
				}

		return render(request, 'createevent.html', context)
	#permission_classes = [owner]



def event_detail(request, event_id):
	event = Event.objects.get(id=event_id)
	context = {
		"event": event,
	}
	return render(request, 'event_detail.html', context)



#

def event_update(request, event_id):
	#Complete Me
	event_obj = Event.objects.get(id=event_id)
	form = EventForm(instance=event_obj)
	if request.method == "POST":
		form = EventForm(request.POST, instance=event_obj)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your car was updated success.')
			return redirect('dashboard')
	context = {
			"event_obj": event_obj,
			"form":form,
			}
	#messages.set_level(request, messages.WARNING)

	#CRITICAL = 50
	#messages.add_message(request, CRITICAL, 'A serious error occurred.')
	return render(request, 'event_update.html', context)


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")
