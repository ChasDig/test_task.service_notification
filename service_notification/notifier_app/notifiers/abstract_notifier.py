from abc import ABC, abstractmethod

from notifier_app.models import User


class AbstractNotifier(ABC):
    """Интерфейс - оповещение."""

    def __init__(self, user: User, message: str) -> None:
        self._user = user
        self._message = message

    @abstractmethod
    def notify(self, *args, **kwargs) -> None:
        pass
