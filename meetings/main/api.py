from main.models import MeetingRoom, Reservation, ReservationInvite
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from dateutil.parser import parse
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (MeetingRoomSerializer, ReservationSerializer, ReservationInviteSerializer,
                          CancelReservationSerializer, AcceptInvitationSerializer, DeclineInvitationSerializer)

from django.http import JsonResponse
import string


class MeetingRoomViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    http_request_methods = ['get', 'post', 'delete']

    def delete(self, request, pk):
        room = self.get_object()
        reservations = ReservationSerializer(Reservation.objects.all().filter(
            room_id=room.room_id, status=0), many=True).data

        if reservations:
            for reservation in reservations:
                if parse(reservation['date_from']).astimezone(timezone.get_current_timezone()) <= timezone.localtime(timezone.now()) <= parse(reservation['date_to']).astimezone(timezone.get_current_timezone()):
                    return Response({'status': "Cannot delete this room, there's on-going reservation"}, status=status.HTTP_400_BAD_REQUEST)
        room.delete()
        return Response({'status': "Meeting Room was successfully deleted"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()


class ReservationViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer
    http_request_methods = ['get', 'post']

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_reservation(self, request, pk=None):
        reservation = self.get_object()

        serializer = CancelReservationSerializer(
            data=request.data,
            context={
                "user": request.user,
                "reservation": reservation,
            },
        )

        if serializer.is_valid():
            result = serializer.save()
            return Response({'status': 'Reservation was cancelled'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Reservation.objects.all()
        employee = self.request.query_params.get('employee_id', None)
        if employee is not None and employee != '':
            if employee in string.digits:
                queryset = queryset.filter(organizer=employee)
        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class ReservationInviteViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ReservationInvite.objects.all()
    serializer_class = ReservationInviteSerializer
    http_request_methods = ['get', 'post']

    @action(detail=True, methods=['get'], url_path='accept')
    def accept_invite(self, request, pk=None):
        invite = self.get_object()

        serializer = AcceptInvitationSerializer(
            data=request.data,
            context={
                "user": request.user,
                "invite": invite,
            },
        )

        if serializer.is_valid():
            result = serializer.save()
            return Response({'status': 'Invitation was accepted'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='decline')
    def decline_invite(self, request, pk=None):
        invite = self.get_object()

        serializer = DeclineInvitationSerializer(
            data=request.data,
            context={
                "user": request.user,
                "invite": invite,
            },
        )

        if serializer.is_valid():
            result = serializer.save
            return Response({'status': 'Invitation was declined'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
