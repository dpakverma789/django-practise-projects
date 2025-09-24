from rest_framework import serializers
from .models import *


class ShowDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowDetails
        fields = '__all__'


class TheaterDetailsSerializer(serializers.ModelSerializer):
    show_name = serializers.CharField(source='show_details.name', read_only=True)
    available_seats = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TheaterDetails
        fields = [
            "id", "theater_name", "show_details", "show_name", "show_time",
            "capacity", "per_seat_price", "reserved_seats", "unreserved_seats", "available_seats"
        ]

    def get_available_seats(self, obj):
        return obj.unreserved_seats


class BookingCreateSerializer(serializers.ModelSerializer):
    # User inputs
    show_name = serializers.CharField(write_only=True)
    theater_name = serializers.CharField(write_only=True)
    show_time = serializers.CharField(write_only=True)

    # Display fields
    booked_show = serializers.CharField(source='show_details.name', read_only=True)
    booked_theater = serializers.CharField(source='theater_details.theater_name', read_only=True)
    booked_show_time = serializers.CharField(source='theater_details.show_time', read_only=True)
    per_seat_price = serializers.IntegerField(source='theater_details.per_seat_price', read_only=True)
    total_amount = serializers.SerializerMethodField(read_only=True)

    def get_total_amount(self, obj):
        """Calculate and return total amount"""
        return obj.reserved_seats * obj.theater_details.per_seat_price

    class Meta:
        model = BookingDetails
        fields = [
            "id",
            # Input fields
            "show_name", "theater_name", "show_time", "name", "reserved_seats",
            # Output fields
            "booked_show", "booked_theater", "booked_show_time", "per_seat_price", "total_amount"
        ]

    def validate(self, data):
        show_name = data.get('show_name')
        theater_name = data.get('theater_name')
        show_time = data.get('show_time')
        reserved_seats = data.get('reserved_seats')

        # Find show
        try:
            show = ShowDetails.objects.get(name__iexact=show_name.strip())
            data['show_details'] = show
        except ShowDetails.DoesNotExist:
            available_shows = ShowDetails.objects.values_list('name', flat=True)
            raise serializers.ValidationError({
                "error": f"Show '{show_name}' not found.",
                "available_shows": list(available_shows),
                "hint": "Check spelling or see available shows at /api/showbox/shows/"
            })

        # Find theater for this show and time
        try:
            theater = TheaterDetails.objects.get(
                theater_name__iexact=theater_name.strip(),
                show_time__iexact=show_time.strip(),
                show_details=show
            )
            data['theater_details'] = theater
        except TheaterDetails.DoesNotExist:
            # Suggest available options
            available_options = TheaterDetails.objects.filter(
                show_details=show
            ).values('theater_name', 'show_time', 'unreserved_seats')

            raise serializers.ValidationError({
                "error": "Combination not found.",
                "requested": {
                    "show": show_name,
                    "theater": theater_name,
                    "show_time": show_time
                },
                "available_options": list(available_options)
            })

        # Seat validation
        if reserved_seats <= 0:
            raise serializers.ValidationError("Must book at least 1 seat.")

        if reserved_seats > theater.unreserved_seats:
            raise serializers.ValidationError({
                "error": "Not enough seats available.",
                "available_seats": theater.unreserved_seats,
                "requested_seats": reserved_seats,
                "suggestion": f"Try booking {theater.unreserved_seats} seats or less."
            })

        return data

    def create(self, validated_data):
        # Remove temporary fields
        validated_data.pop('show_name')
        validated_data.pop('theater_name')
        validated_data.pop('show_time')

        # Calculate amount
        theater = validated_data['theater_details']
        reserved_seats = validated_data['reserved_seats']
        validated_data['amount'] = reserved_seats * theater.per_seat_price

        return super().create(validated_data)