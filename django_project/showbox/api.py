from rest_framework import generics
from .models import ShowDetails, TheaterDetails, BookingDetails
from .serializers import ShowDetailsSerializer, TheaterDetailsSerializer, BookingDetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
"""
ListAPIView → GET all only.
CreateAPIView → POST only.
RetrieveAPIView → Get one only.
UpdateAPIView → PUT/Patch only.
DestroyAPIView → DELETE only.


perform_create(self, serializer): When to use: When you need to modify how an object is saved during creation.
perform_update(self, serializer): When to use: Custom logic during object updates.
get_queryset(): When to use: Dynamic filtering, permission-based data access, or custom query logic.
get_serializer_class(): When to use: Different serializers for different actions or conditions.
get_serializer_context(): When to use: Pass additional context to serializer.

"""

class ShowDetailsAPI(generics.ListCreateAPIView):
    serializer_class = ShowDetailsSerializer

    def get_queryset(self):
        queryset = ShowDetails.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class TheaterDetailsAPI(generics.ListCreateAPIView):
    serializer_class = TheaterDetailsSerializer

    def get_queryset(self):
        queryset = TheaterDetails.objects.all()
        theater = self.request.query_params.get('theater')
        if theater:
            queryset = queryset.filter(theater_name__icontains=theater)
        return queryset


class BookingDetailsAPI(generics.ListCreateAPIView):
    queryset = BookingDetails.objects.all()
    serializer_class = BookingDetailsSerializer

    def perform_create(self, serializer):
        seat_required = serializer.validated_data['reserved_seats']
        theater_details = serializer.validated_data['theater_details']
        amount = seat_required * theater_details.per_seat_price
        if seat_required > theater_details.capacity:
            return Response(
                {"error": f"Booking failed. Theater capacity is {theater_details.capacity}, requested {seat_required} seats."},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking = serializer.save(amount=amount)
        with transaction.atomic():
            # Save the booking
            serializer.save()

            # Update theater seat counts
            # theater_details.unreserved_seats -= seat_required
            # theater_details.reserved_seats += seat_required
            # theater_details.save()
