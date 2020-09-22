from django.urls import path
from .views import Login, Logout, Signup, home
from events import views
from events.views import ListAPIView
from events import views as api_views

#from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('dashboard/', views.Dashboard, name='dashboard'),
	path('create/event/', views.event_create, name='event'),
	path('event/<int:event_id>/', views.event_detail, name='event-detail'),
	path('event/<int:event_id>/update/', views.event_update, name='event-update'),
	path('event/booking/',views.booking_event,name='booking-event'),
	#path('event/booking/<int:event_id>/',views.booking_event_button,name='booking-eventbutton'),
    path('profile/<int:user_id>/update/', views.profile_update, name='profile-update'),

	path('profile', views.profile, name='profile-user'),
	path('login/api/', TokenObtainPairView.as_view(), name='api-login'),
    path('rigester/', api_views.Rigester.as_view(), name='api-register'),
    path('event/create/', api_views.EventCreate.as_view(), name='event-create'),
	path('api/detail/<int:event_id>/', api_views.EventDetailView.as_view(), name='api-detail'),
	path('api/update/<int:event_id>/', api_views.EventUpdateView.as_view(), name='api-update'),
	path('api/bookingevent/', api_views.BookingEventCreate.as_view(), name='api-booking'),
	#path('listuserbooking/', api_views.EventbookingListView.as_view() , name='api-userbooking'),


	#path('list/', EventListView.as_view(), name='list'),


	path('eventList/', api_views.EventListView.as_view(), name='Event-list'),



]
