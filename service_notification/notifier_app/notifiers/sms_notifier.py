from django.conf import settings
from twilio.rest import Client

from .abstract_notifier import AbstractNotifier
from notifier_app.models import User
from notifier_app.utils.custom_exseptions import SMSNotificationError


class SMSNotifier(AbstractNotifier):
    """Интерфейс - отправка оповещения по SMS."""

    def __init__(self, user: User, message: str):
        super().__init__(user=user, message=message)
        self._client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

    def notify(self) -> None:
        if phone_number := self._user.phone_number:
            try:
                self._client.messages.create(
                    body=self._message,
                    from_=settings.TWILIO_PHONE,
                    to=phone_number,
                )

            except Exception as ex:
                raise SMSNotificationError(ex) from ex

        else:
            raise SMSNotificationError("user have not phone number")
