from django.contrib import admin
from . import models

admin.site.register(models.BookingDetails)
admin.site.register(models.TheaterDetails)
admin.site.register(models.ShowDetails)