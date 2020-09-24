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
from .serializers import  ListEventSerializer , CreateEventSerializer , RigesterSerializer , ListBookingEventSerializer , EventDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import  IsAuthenticated, IsAdminUser ,AllowAny
from rest_framework.filters import OrderingFilter ,SearchFilter


class Rigester(CreateAPIView):
    serializer_class = RigesterSerializer


class EventListView(ListAPIView): # list upcoming event
    queryset = Event.objects.filter(date_event__gt=date.today())
    serializer_class = ListEventSerializer
    filter_backends = [SearchFilter,]
    search_fields = ['organizer__username',] # you can retrive list of specfic organizer


class EventBookingListView(ListAPIView): # list of booking by user
    queryset = BookingEvent.objects.all()
    serializer_class = ListBookingEventSerializer
    filter_backends = [SearchFilter,]  # you can retrive list of specfic user
    search_fields = ['user__username',]





class EventDetailView(RetrieveAPIView):# list of user booking this event
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'


class BookingEventCreate(CreateAPIView):#
    #permission_classes = [IsAdminUser]
    queryset = Event.objects.all()
    serializer_class = ListBookingEventSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class EventCreate(CreateAPIView):# just admin
    permission_classes = [IsAdminUser]
    serializer_class = CreateEventSerializer
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventUpdateView(RetrieveUpdateAPIView):# just admin
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsAdminUser]

##########################################END_API#################
def profile(request):
    username=request.user
    #booking_event=BookingEvent.objects.filter(user=username)
    eventsupcoming=Event.objects.filter(date_event__gte=date.today())
    events=Event.objects.filter(date_event__lt=date.today())
    booking_event=BookingEvent.objects.filter(user=username )

    context = {
        "events": events,
        "eventsupcoming" :eventsupcoming,
        "booking_event": booking_event,
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






def Dashboard(request):
    if  request.user.is_staff:
        event= Event.objects.all()
    else:
        event=Event.objects.filter(date_event__gt=date.today())

    query = request.GET.get("q")
    if query:
        event = event.filter(Q(title__icontains=query)|
            Q(description__icontains=query)|Q(organizer__username__icontains=query)
            ).distinct()

    context = {
            "events": event,
            #"eventupcoming":eventupcoming,
        }
    return render(request, 'dashboard.html', context)

def event_create(request):


        form = EventForm()
        if request.method == "POST":
            form = EventForm(request.POST ,request.FILES )
            if form.is_valid():
                form=form.save(commit=False)
                form.organizer=request.user
                form.save()
                messages.success(request, ' Add  Success.')
                return redirect('dashboard')

        context = {
                "form":form,
                }

        return render(request, 'createevent.html', context)




def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)


    list_of_booking=BookingEvent.objects.filter(event=event)
    context = {
        "event": event,
        "list_of_booking":list_of_booking,
    }
    return render(request, 'event_detail.html', context)



#

def profile_update(request):
#, user_id):
    #Complete Me
    #user_obj = User.objects.get(id=user_id) # change to  request.user to more secure
    user_obj = User.objects.get(username=request.user)
    user_id=user_obj.id
    user_obj = User.objects.get(id=user_id)
    form = UserForm(instance=user_obj)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile was Updated Success.')
            return redirect('profile-user')
    context = {
            "user_obj": user_obj,
            "form":form,
            }

    return render(request, 'profile_update.html', context)

def event_update(request, event_id):
    #Complete Me
    if request.user.is_staff :
        event_obj = Event.objects.get(id=event_id)
        form = EventForm(instance=event_obj)
        if request.method == "POST":
            form = EventForm(request.POST,request.FILES, instance=event_obj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Event was Updated Success.')
                return redirect('dashboard')
        context = {
                "event_obj": event_obj,
                "form":form,
                }

        return render(request, 'event_update.html', context)



def event_delete(request, event_id):
	#Complete Me
	event_obj = Event.objects.get(id=event_id)
	event_obj.delete()
	messages.success(request, ' Delete  Success.')
	return redirect('dashboard')

def booking_event(request , event_id):
    event_obj = Event.objects.get(id=event_id) #edit
    event_name=event_obj.title


    form = BookingEventForm()

    if request.method == "POST":
                form = BookingEventForm(request.POST )
                if form.is_valid():
                    form=form.save(commit=False)
                    form.user=request.user
                    form.event=event_obj # edit
                    event=form.event
                    if event.seats >= form.ticketnumber:
                        update_seats=event.seats-form.ticketnumber
                        event.seats= update_seats
                        event.save()
                        form.save()
                        messages.success(request, ' Booking  Success.')
                    else:
                        messages.success(request, ' This Event is FULL!!')

                    return redirect('dashboard')

    context = {
                    "form":form,
                    "event_obj":event_obj,
                    }

    return render(request, 'booking_event.html', context)





class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")
