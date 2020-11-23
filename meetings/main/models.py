from django.db import models
from datetime import date, datetime, time, timedelta
from accounts.models import Employees
from main.validators import validate_date_from, validate_date_to
import uuid


""" * So my logic to check the room avaibility is by
    checking if there are no active reservations by the time
    when API request is sent.
"""


class MeetingRoom(models.Model):
    # I will not create a status field, I'm going to manipulate it...
    room_id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    room_number = models.CharField(
        max_length=16,
        unique=True
    )

    class Meta:
        db_table = "MeetingRooms"

    def __str__(self):
        return str(self.room_id)


class Reservation(models.Model):
    STATUS_VALID = 0
    STATUS_CANCELLED = 1
    STATUS_TYPES = [
        (STATUS_VALID, "Valid"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    meeting_id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    room_id = models.ForeignKey(
        MeetingRoom,
        related_name="reservations",
        on_delete=models.CASCADE
    )
    organizer = models.ForeignKey(
        Employees,
        related_name="organized_reservations",
        on_delete=models.CASCADE
    )
    invites = models.ManyToManyField(
        Employees,
        through="ReservationInvite"
    )
    title = models.CharField(max_length=150, blank=False, null=False)
    status = models.IntegerField(
        choices=STATUS_TYPES,
        default=STATUS_VALID
    )
    date_from = models.DateTimeField(validators=[validate_date_from])
    date_to = models.DateTimeField(validators=[validate_date_to])

    class Meta:
        db_table = "Reservations"

    def __str__(self):
        return str(self.meeting_id)


class ReservationInvite(models.Model):
    IS_PENDING = -1
    IS_ATTENDING = 1
    IS_NOT_ATTENDING = 0
    ATTENDING_STATUSES = [
        (IS_PENDING, "Pending"),
        (IS_ATTENDING, "Attending"),
        (IS_NOT_ATTENDING, "Not attending")
    ]

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        Employees,
        related_name="invited_reservations",
        on_delete=models.CASCADE
    )
    status = models.IntegerField(
        choices=ATTENDING_STATUSES,
        default=IS_PENDING
    )

    class Meta:
        db_table = "ReservationInvites"

    def __str__(self):
        return str(self.id)
