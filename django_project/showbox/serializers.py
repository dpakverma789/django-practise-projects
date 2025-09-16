from rest_framework import serializers
from .models import ShowDetails,BookingDetails

class ShowDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowDetails
        fields = '__all__'

class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDetails
        fields = '__all__'