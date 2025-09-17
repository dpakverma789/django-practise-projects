from django.http import HttpResponse
from django.views import View
from .models import *


class Bookings(View):
    def get(self, request):
        table_data = ''
        booking_details = BookingDetails.objects.all()
        for i in booking_details:
            table_data += f"""
                <tr>
                  <td>{i.name}</td>
                  <td>{i.reserved_seats}</td>
                  <td>{i.amount}</td>
                  <td>{i.theater_details.name}</td>
                  <td>{i.show_details.name}</td>
                  <td>{i.show_details.show_time}</td>
                </tr>
            """
        table = f"""
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Booking Name</th>
              <th scope="col">Booked Seats</th>
              <th scope="col">Amount Paid</th>
              <th scope="col">Show Name</th>
              <th scope="col">Show Time</th>
            </tr>
          </thead>
          <tbody>
            {table_data}
          </tbody>
        </table>
        """
        return HttpResponse(table)
