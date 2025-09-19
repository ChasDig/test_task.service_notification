from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .tasks import send_notification
from .serializers import NotificationSerializer


# --- Notify User --- #
class NotificationUserView(APIView):
    """View - отправка оповещения пользователю."""

    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        send_notification.delay(**serializer.validated_data)
        return Response(
            data={
                "status": "queued",
            },
            status=status.HTTP_202_ACCEPTED,
        )
