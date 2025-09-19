from django.conf import settings
from django.core.mail import send_mail

from .abstract_notifier import AbstractNotifier
from notifier_app.utils.custom_exseptions import EmailNotificationError


class EmailNotifier(AbstractNotifier):
    """Интерфейс - отправка оповещения по Email."""

    def notify(self) -> None:
        if to_email := self._user.email:
            try:
                send_mail(
                    "Notification",
                    self._message,
                    settings.EMAIL_HOST_USER,
                    [to_email, ],
                )

            except Exception as ex:
                raise EmailNotificationError() from ex

        else:
            raise EmailNotificationError("user have not email")