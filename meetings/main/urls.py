from django.conf.urls import url
from knox import views as knox_views
from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from .api import MeetingRoomViewset, ReservationViewset, ReservationInviteViewset
from main import views

from accounts.api import RegisterAPI, LoginAPI, UserAPI

# Import other API routes from accounts app
from accounts.urls import router as accountrouter

router = routers.DefaultRouter()
router.registry.extend(accountrouter.registry)
router.register('rooms', MeetingRoomViewset, 'rooms')
router.register('invites', ReservationInviteViewset, 'invites')
router.register('reservations', ReservationViewset, 'reservations')

urlpatterns = [
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
    path('auth/user', UserAPI.as_view()),
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]

urlpatterns += router.urls
