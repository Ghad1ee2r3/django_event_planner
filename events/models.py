from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone




class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    date_event= models.DateField(default=timezone.now)

    organizer=models.ForeignKey(User, on_delete=models.CASCADE ,default=1 )
    location=models.CharField(max_length=150)
    seats=models.IntegerField()
    img=models.ImageField(upload_to='event', null=True, blank=True )

    def __str__(self):
        return self.title

        

class BookingEvent(models.Model):

    user=models.ForeignKey(User, on_delete=models.CASCADE ,default=1 )
    event=models.ForeignKey(Event, on_delete=models.CASCADE ,default=1 )

    ticketnumber=models.IntegerField()









    def __str__(self):
        return self.event.title
