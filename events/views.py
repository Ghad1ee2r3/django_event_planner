from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin ,EventForm , BookingEventForm ,UserForm
from django.contrib import messages
from .models import Event ,BookingEvent
from .permissions import owner
from datetime import date
from django.db.models import Q
from django.contrib.auth.models import User


##########################################API#################
from .serializers import  ListEventSerializer , CreateEventSerializer , RigesterSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import  IsAuthenticated, IsAdminUser ,AllowAny
from rest_framework.filters import OrderingFilter ,SearchFilter


class Rigester(CreateAPIView):
    serializer_class = RigesterSerializer


class EventListView(ListAPIView): # list upcoming event
    queryset = Event.objects.filter(date_event__gt=date.today())
    serializer_class = ListEventSerializer
    filter_backends = [SearchFilter,]
    search_fields = ['organizer__username',]


class EventCreate(CreateAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class = CreateEventSerializer
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

##########################################END_API#################
def profile(request):
    username=request.user
    #booking_event=BookingEvent.objects.filter(user=username)
    events=Event.objects.filter(date_event__lt=date.today())
    booking_event=BookingEvent.objects.filter(user=username )
    #date=date.today()
    #,event.date_event__lt==date.today() )
    #date=datetime.now()
    #c="2020-09-09"
    #a=timezone.now
    #current=Memberships.objects.filter(datereturn=d)

    context = {
        "events": events,

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
            Q(description__icontains=query)|Q(organizer__username__icontains=query)
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
                form=form.save(commit=False)
                form.organizer=request.user
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
    list_of_booking=BookingEvent.objects.filter(event=event)
    context = {
        "event": event,
        "list_of_booking":list_of_booking,
    }
    return render(request, 'event_detail.html', context)



#

def profile_update(request, user_id):
    #Complete Me
    user_obj = User.objects.get(id=user_id)
    form = UserForm(instance=user_obj)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated success.')
            return redirect('profile-user')
    context = {
            "user_obj": user_obj,
            "form":form,
            }
    #messages.set_level(request, messages.WARNING)

    #CRITICAL = 50
    #messages.add_message(request, CRITICAL, 'A serious error occurred.')
    return render(request, 'profile_update.html', context)

def event_update(request, event_id):
    #Complete Me
    event_obj = Event.objects.get(id=event_id)
    form = EventForm(instance=event_obj)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your event was updated success.')
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
            #b=0
            if request.method == "POST":
                form = BookingEventForm(request.POST )
                if form.is_valid():
                    form=form.save(commit=False)
                    form.user=request.user
                    event=form.event
                    if event.seats >= form.ticketnumber:
                        update_seats=event.seats-form.ticketnumber
                        event.seats= update_seats
                        event.save()
                        form.save()
                        messages.success(request, ' booking  success.')
                    else:
                        messages.success(request, ' This Event is FULL!!')

                    return redirect('dashboard')
                #else:
                #    messages.success(request, ' not  success.')
            context = {
                    "form":form,
                    #"a":a
                    }

            return render(request, 'booking_event.html', context)



###################################################################test###########################################3
#def booking_event_button(request ,event_id):
#    event_obj = Event.objects.get(id=event_id)
#    event = Event.objects.get(id=event_id)

#    form = BookingEventForm()
#    if request.method == "POST":
#        form = BookingEventForm(request.POST )
#        if form.is_valid():
#                    form=form.save(commit=False)
#                    form.event=event
#                    form.user=request.user
#                   form.save()
#                    messages.success(request, ' booking  success.')
#                    return redirect('dashboard')
                #else:
                #    messages.success(request, ' not  success.')
#        context = {
#                    "form":form,
#                    "event":event ,
#                    }

        #return render(request, 'booking_event.html', context)

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")
