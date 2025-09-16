# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ShowDetails, BookingDetails
from .serializers import ShowDetailsSerializer, BookingDetailsSerializer

class Shows(APIView):
    def get(self, request):
        shows = ShowDetails.objects.all()
        serializer = ShowDetailsSerializer(shows, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShowDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Bookings(APIView):
    def get(self, request):
        # booking = BookingDetails.objects.all()
        # serializer = BookingDetailsSerializer(booking, many=True)
        # return Response(serializer.data)
        bookings = BookingDetails.objects.select_related('show_booking').all()
        data = []
        for booking in bookings:
            data.append({
                'theater_name': booking.theater_name,
                'movie_name': booking.show_booking.show_name,
                'show_time': booking.show_booking.show_time,
                'unbook_seats': booking.unbook_seats,
                'amount': booking.amount,
            })

        return Response(data)

    def post(self, request):
        serializer = BookingDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
