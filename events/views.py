from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin ,EventForm , BookingEventForm
from django.contrib import messages
from .models import Event , Dashboard ,BookingEvent
from .permissions import owner
from datetime import date
from django.db.models import Q




def profile(request):
    username=request.user
    booking_event=BookingEvent.objects.filter(user=username)
    #date=datetime.now()
    #c="2020-09-09"
    #a=timezone.now
    #current=Memberships.objects.filter(datereturn=d)

    context = {
        #"current": current,
        "booking_event": booking_event
    }
    return render(request, 'profile.html', context)



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
#    user = Dashboard.objects.get(id=user_id)
#    if  not request.user==user.owner:
#        eventupcoming=Event.objects.filter(date_event__gt=date.today())
        #event = Event.objects.all()
#        context = {
                #"events": event,
#                "eventupcoming":eventupcoming,
#            }
#        return render(request, 'dashboard.html', context)


def Dashboard(request):
    if  request.user.is_staff:
        event= Event.objects.all()
    else:
        event=Event.objects.filter(date_event__gt=date.today())
    #event = Event.objects.all()
    #owner =event.organizer.owner
    query = request.GET.get("q")
    if query:
        event = event.filter(Q(title__icontains=query)|
            Q(description__icontains=query)|Q(organizer__owner__username__icontains=query)
            ).distinct()
        #event=Dashboard.objects.filter()
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

    title_event=event.title
    list_of_booking=BookingEvent.objects.filter(nameEvent=title_event)
    context = {
        "event": event,
        "list_of_booking":list_of_booking,
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

def booking_event(request ):
#    event_obj = Event.objects.get(id=event_id)

            form = BookingEventForm()
            if request.method == "POST":
                form = BookingEventForm(request.POST )
                if form.is_valid():
                    form=form.save(commit=False)
                    form.user=request.user
                    form.save()
                    messages.success(request, ' booking  success.')
                    return redirect('dashboard')
                #else:
                #    messages.success(request, ' not  success.')
            context = {
                    "form":form,
                    }

            return render(request, 'booking_event.html', context)

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")
