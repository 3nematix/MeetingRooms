from datetime import datetime
from dateutil.parser import parse
from django.utils import timezone
from rest_framework import serializers
from main.models import MeetingRoom, Reservation, ReservationInvite
from accounts.models import Employees
from accounts.serializers import EmployeeSerializer

""" I think it's not really necessary (in this case) to implement the validation logic
    on the model layer, so I wrote it on the serializer layer. 

    * However, the validation logic is BETTER when it's in the model layer, it
    also protects from users/hackers if they would somehow get access to back-end api endpoints.
"""


class MeetingRoomSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = MeetingRoom
        fields = '__all__'

    def get_status(self, obj):
        reservations = ReservationSerializer(Reservation.objects.all().filter(
            room_id=obj.room_id, status=0), many=True).data
        if reservations:
            for reservation in reservations:
                if parse(reservation['date_from']).astimezone(timezone.get_current_timezone()) <= timezone.localtime(timezone.now()) <= parse(reservation['date_to']).astimezone(timezone.get_current_timezone()):
                    return False
        return True


class CancelReservationSerializer(serializers.Serializer):
    def save(self):
        user = self.context.get("user")
        reservation = self.context.get("reservation")

        if user == reservation.organizer:
            if reservation.status is 0:
                reservation.status = 1
                reservation.save()
                return ReservationSerializer(reservation)
            raise serializers.ValidationError(
                {"error": "Reservation is already cancelled"})

        raise serializers.ValidationError(
            {"error": "User is not an organizator"})


class ReservationSerializer(serializers.ModelSerializer):

    organizer = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    invites = serializers.SerializerMethodField()

    class Meta:

        model = Reservation
        fields = (
            'meeting_id',
            'room_id',
            'organizer',
            'invites',
            'title',
            'status',
            'date_from',
            'date_to',
        )
        extra_kwargs = {'title': {'min_length': 8}}
        read_only_fields = ('meeting_id', 'invites', 'status')

    def get_invites(self, obj):
        return ReservationInviteSerializer(ReservationInvite.objects.all().filter(reservation=obj), many=True).data

    def get_organizer(self, obj):
        return EmployeeSerializer(obj.organizer).data

    def get_status(self, obj):
        return obj.get_status_display()

    def validate(self, data):

        # We convert the provided date & time to our local server timezone (UTC+3)

        wanted_date_from = data['date_from'].astimezone(
            timezone.get_current_timezone())
        wanted_date_to = data['date_to'].astimezone(
            timezone.get_current_timezone())

        # Check if the reservation starting time isn't greater than reservation ending time.
        if wanted_date_to <= wanted_date_from:
            raise serializers.ValidationError(
                "Meeting could not end earlier than it starts")

        # Check if there are any other VALID reservations by that time range.
        reservations = Reservation.objects.all().filter(
            room_id=data['room_id'], status=0)
        if reservations:
            for reservation in reservations:
                if reservation.date_from.astimezone(timezone.get_current_timezone()) <= wanted_date_from <= reservation.date_to.astimezone(timezone.get_current_timezone()) or reservation.date_from.astimezone(timezone.get_current_timezone()) <= wanted_date_to <= reservation.date_to.astimezone(timezone.get_current_timezone()):
                    raise serializers.ValidationError(
                        "This time is being used by another reservation")

        return data


class ReservationInviteSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = ReservationInvite
        fields = '__all__'
        extra_kwargs = {'employee': {'write_only': True}}
        read_only_fields = ('id', 'receiver')

    def get_status(self, obj):
        return obj.get_status_display()

    def get_receiver(self, obj):
        return EmployeeSerializer(obj.employee).data

    def validate_employee(self, obj):
        user = self.context['request'].user
        if user.pk == obj.pk:
            raise serializers.ValidationError("You cannot invite yourself")
        return obj

    def validate(self, data):
        # We can't invite people if the reservation status is 1
        if data['reservation'].status is 1:
            raise serializers.ValidationError(
                'You cannot invite people to cancelled reservation')

        for employee in data['reservation'].invites.all():
            if employee == data['employee']:
                raise serializers.ValidationError(
                    'This user is already invited')
        return data


class AcceptInvitationSerializer(serializers.Serializer):
    def save(self):
        user = self.context.get("user")
        invite = self.context.get("invite")

        # Check if the reservation isn't canceled
        if invite.reservation.status is 0:
            if user == invite.employee:
                invite.status = 1
                invite.save()
                return ReservationInvite(invite)

            raise serializers.ValidationError(
                {"error": "Employee is not the receiver"})

        raise serializers.ValidationError(
            {"error": "Reservation was cancelled"})


class DeclineInvitationSerializer(serializers.Serializer):
    def save(self, validated_data):
        user = self.context.get("user")
        invite = self.context.get("invite")

        if invite.reservation.status is 0:
            if user == invite.employee:
                invite.status = 0
                invite.save()
                return ReservationInvite(invite)

            raise serializers.ValidationError(
                {"error": "Employee is not the receiver"})
        raise serializers.ValidationError(
            {"error": "Reservation was cancelled"})
