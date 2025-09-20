from django.urls import path
from .api import ShowDetailsAPI, TheaterDetailsAPI, BookingDetailsAPI

urlpatterns = [
    path('shows/', ShowDetailsAPI.as_view()),
    path('theater/', TheaterDetailsAPI.as_view()),
    path('booking/', BookingDetailsAPI.as_view()),
]
