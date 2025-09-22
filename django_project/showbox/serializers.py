from rest_framework import serializers
from .models import *
class ShowDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowDetails
        fields = '__all__'


class TheaterDetailsSerializer(serializers.ModelSerializer):
    show_name = serializers.CharField(source='show_details.name', read_only=True)
    class Meta:
        model = TheaterDetails
        fields = ["id","theater_name","show_details","show_name","show_time",
                  "capacity","per_seat_price","reserved_seats","unreserved_seats"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    show_time = serializers.CharField(source='theater_details.show_time', read_only=True)
    theater_name = serializers.CharField(source='theater_details.theater_name', read_only=True)
    show_name = serializers.CharField(source='show_details.name', read_only=True)

    class Meta:
        model = BookingDetails
        fields = ["id","theater_details","theater_name","name","show_details","show_name","show_time","reserved_seats","amount"]