from django.urls import path
from .views import *

urlpatterns = [
    path('booking/', Bookings.as_view(), name='Bookings'),
]
