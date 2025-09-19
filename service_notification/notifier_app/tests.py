import pytest

from notifier_app.models import User
from notifier_app.notifiers import TelegramNotifier, SMSNotifier, EmailNotifier
from notifier_app.utils.custom_exseptions import (
    TelegramNotificationError,
    SMSNotificationError,
    EmailNotificationError
)


# --- TelegramNotifier --- #
def test_telegram_notify_success(mocker) -> None:
    """
    Тест - проверка отправки сообщения через Телеграм.

    :param mocker:
    :type mocker:

    :return:
    :rtype: None
    """
    user = User(telegram_id=12345)
    mock_send = mocker.patch("notifier_app.notifiers.telegram.Bot.sendMessage")
    notifier = TelegramNotifier(user, "Hello")
    notifier.notify()
    mock_send.assert_called_once_with(chat_id=12345, text="Hello")


def test_telegram_notify_no_id() -> None:
    """
    Тест - проверка отработки исключения, если у пользователя не найден
    telegram_id при отправке сообщения через Телеграм.

    :return:
    :rtype: None
    """
    user = User(telegram_id=None)
    notifier = TelegramNotifier(user, "Hello")
    with pytest.raises(TelegramNotificationError):
        notifier.notify()


# --- SMSNotifier --- #
def test_sms_notify_success(mocker) -> None:
    """
    Тест - проверка отправки сообщения через SMS.

    :param mocker:
    :type mocker:

    :return:
    :rtype: None
    """
    user = User(phone_number="+1234567890")
    mock_client = mocker.patch("notifier_app.notifiers.SMSNotifier._client")
    mock_client.messages.create.return_value = True
    notifier = SMSNotifier(user, "Hello")
    notifier.notify()
    mock_client.messages.create.assert_called_once_with(
        body="Hello",
        from_=mocker.ANY,
        to="+1234567890",
    )


def test_sms_notify_no_phone():
    """
    Тест - проверка отработки исключения, если у пользователя не найден
    phone_number при отправке сообщения через SMS.

    :return:
    :rtype: None
    """
    user = User(phone_number=None)
    notifier = SMSNotifier(user, "Hello")
    with pytest.raises(SMSNotificationError):
        notifier.notify()


# --- EmailNotifier --- #
def test_email_notify_success(mocker) -> None:
    """
    Тест - проверка отправки сообщения через Email.

    :param mocker:
    :type mocker:

    :return:
    :rtype: None
    """
    user = User(email="test@example.com")
    mock_send_mail = mocker.patch("notifier_app.notifiers.send_mail")
    notifier = EmailNotifier(user, "Hello")
    notifier.notify()
    mock_send_mail.assert_called_once_with(
        "Notification",
        "Hello",
        mocker.ANY,
        ["test@example.com"],
    )


def test_email_notify_no_email() -> None:
    """
    Тест - проверка отработки исключения, если у пользователя не найден
    email при отправке сообщения через Email.

    :return:
    :rtype: None
    """
    user = User(email=None)
    notifier = EmailNotifier(user, "Hello")
    with pytest.raises(EmailNotificationError):
        notifier.notify()
