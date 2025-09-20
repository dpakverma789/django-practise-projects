from rest_framework import serializers
from .models import *

class BookingDetailsSerializer(serializers.ModelSerializer):
    show_name = serializers.CharField(source='show_details.name', read_only=True)
    theater_name = serializers.CharField(source='theater_details.name', read_only=True)
    class Meta:
        model = BookingDetails
        fields = [
            "id",
            "name",
            "reserved_seats",
            "amount",
            "show_name",
            "theater_name"
        ]


class ShowDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowDetails
        fields = ["id", "name", "show_time"]


class TheaterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterDetails
        fields = ["id", "name", "capacity", "reserved_seats", "unreserved_seats"]