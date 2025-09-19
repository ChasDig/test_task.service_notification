from telegram import Bot
from django.conf import settings

from .abstract_notifier import AbstractNotifier
from notifier_app.models import User
from notifier_app.utils.custom_exseptions import TelegramNotificationError


class TelegramNotifier(AbstractNotifier):
    """Интерфейс - отправка оповещения через Telegram."""

    def __init__(self, user: User, message: str):
        super().__init__(user=user, message=message)
        self._bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    def notify(self) -> None:
        if chat_id := self._user.telegram_id:
            try:
                self._bot.sendMessage(
                    chat_id=chat_id,
                    text=self._message,
                )

            except Exception as ex:
                raise TelegramNotificationError(ex) from ex

        else:
            raise TelegramNotificationError("user have not telegram_id")
