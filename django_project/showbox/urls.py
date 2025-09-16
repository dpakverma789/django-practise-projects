from django.urls import path
from .views import *

urlpatterns = [
    path('show/', Shows.as_view(), name='show'),
    path('booking/', Bookings.as_view(), name='Bookings'),
]
