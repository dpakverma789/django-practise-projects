# urls.py
from django.urls import path
from . import api

urlpatterns = [
    path('shows/', api.ShowDetailsAPI.as_view(), name='show-list'),
    path('theaters/', api.TheaterDetailsAPI.as_view(), name='theater-list'),
    path('booking/', api.BookingDetailsAPI.as_view(), name='booking-create'),
]