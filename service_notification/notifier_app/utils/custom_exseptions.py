class BaseNotificationException(Exception):
    """Exception - базовое исключение при оповещении."""


class EmailNotificationError(BaseNotificationException):
    """Exception - исключение при оповещении через Email."""


class SMSNotificationError(BaseNotificationException):
    """Exception - исключение при оповещении через SMS."""


class TelegramNotificationError(BaseNotificationException):
    """Exception - исключение при оповещении через Telegram."""
