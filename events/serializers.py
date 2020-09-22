from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event ,BookingEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name']


class RigesterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name',]

    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(new_user.password)
        new_user.save()
        return new_user



class ListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        #org=Event.organizer.username
        fields ='__all__'
        #['title' , 'description' ,'date_event', 'or' ,'location' ,'seats' ]


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ListBookingEventSerializer(serializers.ModelSerializer):
     #user = UserSerializer()
     #event=CreateEventSerializer()
     #event = serializers.SerializerMethodField()
     class Meta:
        model = BookingEvent
        fields = ['event' , 'user' ,'ticketnumber']
     #def get_event(self, obj):
    #    event = Event.objects.get(id=obj.id)

        #title_event=event.title

        #return CreateEventSerializer(title_event, many=True).data

class EventDetailSerializer(serializers.ModelSerializer):
    booking_by = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['title' ,'date_event' ,'organizer', 'location' ,'seats' ,'description' , 'booking_by' ]
        #'__all__'
    def get_booking_by(self, obj):
        event = Event.objects.get(id=obj.id)

        title_event=event.title
        list_of_booking=BookingEvent.objects.filter(event=event)
        #us = BookingEvent.objects.filter(event= Event.title)
        return UserSerializer(list_of_booking, many=True).data
