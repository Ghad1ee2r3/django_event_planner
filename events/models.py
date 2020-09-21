from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Dashboard(models.Model):
    title = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dashboard")

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    #creation_date = models.DateField(auto_now_add=True)
    date_event= models.DateField(default=timezone.now)
    is_done = models.BooleanField()
    organizer=models.ForeignKey(Dashboard, on_delete=models.CASCADE ,default=1 )
    location=models.CharField(max_length=150)
    seats=models.IntegerField()

    def __str__(self):
        return self.title

class BookingEvent(models.Model):
    #"""docstring for BookingEvent."""
    user=models.ForeignKey(User, on_delete=models.CASCADE ,default=1 )
    nameEvent = models.CharField(max_length=120)
    ticketnumber=models.IntegerField()
    #def __init__(self, arg):
    #    super(BookingEvent, self).__init__()
    #    self.arg = arg








    def __str__(self):
        return self.nameEvent
