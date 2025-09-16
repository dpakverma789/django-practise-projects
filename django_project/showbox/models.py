from django.db import models

class ShowDetails(models.Model):
    name = models.CharField()
    show_time = models.DateTimeField()

    def __str__(self):
        return self.name


class TheaterDetails(models.Model):
    name = models.CharField()
    capacity = models.IntegerField()
    reserved_seats = models.IntegerField()
    unreserved_seats = models.IntegerField()

    def __str__(self):
        return self.name


class BookingDetails(models.Model):
    name = models.CharField()
    reserved_seats = models.IntegerField()
    amount = models.IntegerField(default=0)
    theater_details = models.ForeignKey(TheaterDetails, on_delete=models.CASCADE,db_column="theater_details_id") # M2O
    show_details = models.ForeignKey(ShowDetails, on_delete=models.CASCADE,db_column="show_details_id") # M2O