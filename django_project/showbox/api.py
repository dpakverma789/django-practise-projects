from rest_framework import generics
from .models import ShowDetails, TheaterDetails, BookingDetails
from .serializers import ShowDetailsSerializer, TheaterDetailsSerializer, BookingCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


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
    serializer_class = BookingCreateSerializer

    def get_queryset(self):
        return BookingDetails.objects.select_related('theater_details', 'show_details').all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                theater_details = serializer.validated_data['theater_details']
                seat_required = serializer.validated_data['reserved_seats']

                # Save booking
                booking = serializer.save()

                # Update theater seats
                theater_details.unreserved_seats -= seat_required
                theater_details.reserved_seats += seat_required
                theater_details.save()

                # Return success response with booking summary
                response_data = serializer.data
                response_data.update({
                    "message": "Booking confirmed!",
                    "summary": {
                        "show": booking.show_details.name,
                        "theater": booking.theater_details.theater_name,
                        "show_time": booking.theater_details.show_time,
                        "seats_booked": seat_required,
                        "total_amount": booking.amount
                    }
                })

                return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Booking failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )