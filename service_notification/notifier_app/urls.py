from django.urls import path

from .views import NotificationUserView


urlpatterns = [
    path("notify", NotificationUserView.as_view(), name="notify_user"),
]
