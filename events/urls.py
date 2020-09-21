from django.urls import path
from .views import Login, Logout, Signup, home
from events import views
#from django.conf import settings
#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#)

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
	path('profile', views.profile, name='profile-user'),



]
