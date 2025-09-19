import enum


class NotificationTypeEnum(enum.Enum):
    """Enum - типы оповещений."""

    email = "email"
    sms = "sms"
    telegram = "telegram"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


class NotificationStatusEnum(enum.Enum):
    """Enum - статусы оповещений."""

    success = "success"
    error = "error"
