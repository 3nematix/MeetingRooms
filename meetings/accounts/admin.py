from django.contrib import admin
from accounts.models import Employees
from main.models import MeetingRoom, Reservation, ReservationInvite

# Register your models here.

admin.site.register(Employees)
admin.site.register(MeetingRoom)
admin.site.register(Reservation)
admin.site.register(ReservationInvite)
