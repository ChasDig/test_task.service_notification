import logging
from typing import Callable

from celery import Task
from celery.exceptions import MaxRetriesExceededError

from service_notification.celery import app
from notifier_app.models import User
from notifier_app.notifiers import SMSNotifier, TelegramNotifier, EmailNotifier
from notifier_app.utils.custom_enums import (
    NotificationTypeEnum,
    NotificationStatusEnum,
)
from notifier_app.utils.custom_exseptions import (
    BaseNotificationException,
    EmailNotificationError,
    SMSNotificationError,
    TelegramNotificationError,
)


logger = logging.getLogger("notifier")


class SendNotificationTask(Task):
    """CeleryTask - отправка оповещения/уведомления."""

    name = "notifier_app.tasks.send_notification"

    @property
    def type_to_method(self) -> dict[str, Callable[[User, str], str]]:
        return {
            NotificationTypeEnum.email.value: self._notification_by_email,
            NotificationTypeEnum.sms.value: self._notification_by_sms,
            NotificationTypeEnum.telegram.value: self._notification_by_tg,
        }

    def run(
        self,
        types: list[str],
        to_user_ids: list[int],
        message: str,
        use_other_types_on_error: bool = True,
        max_retries: int = 0,
    ) -> None:
        """
        Точка входа в задачу.

        :param types: Список типов(источников) оповещений.
        :type types: list[str]
        :param to_user_ids:
        :type to_user_ids: list[int]
        :param message:
        :type message: str
        :param use_other_types_on_error: Флаг, требуется ли использовать
        альтернативные источники оповещения, если указанные не выполнились.
        :type use_other_types_on_error: bool
        :param max_retries: Кол-во попыток отправки оповещения.
        :type max_retries: int

        :return:
        :rtype: None
        """
        user_ids_for_retry = list()

        for user in User.objects.filter(id__in=to_user_ids).iterator():
            notify_results = {
                type_: self.type_to_method[type_](user, message)
                for type_ in types if type_ in self.type_to_method
            }

            if use_other_types_on_error:
                try:
                    self._notify_by_other_types_on_error(
                        user,
                        message,
                        notify_results,
                    )

                except BaseNotificationException:
                    if max_retries:
                        user_ids_for_retry.append(user.id)

        if user_ids_for_retry:
            self._retry_notification(max_retries, user_ids_for_retry)

    def _notify_by_other_types_on_error(
        self,
        user: User,
        message: str,
        notify_results: dict[str, str],
    ) -> None:
        """
        Оповещение Пользователя по иным источникам, доступные ему.

        :param user:
        :type user: User
        :param message:
        :type message: str
        :param notify_results: Результат ранее отправленных сообщений по
        каждому источнику.
        :type notify_results: dict[str, str]

        :return:
        :rtype: None
        """
        if all(
            result == NotificationStatusEnum.error.name
            for result in notify_results.values()
        ):
            notify_results_on_error = {
                type_: self.type_to_method[type_](user, message)
                for type_ in self.type_to_method if type_ not in notify_results
            }

            if notify_results_on_error and all(
                result == NotificationStatusEnum.error.name
                for result in notify_results_on_error.values()
            ):
                logger.error(
                    f"[!] Error send message to '{user.username}' by other "
                    "types of notification! Message was not send..."
                )
                raise BaseNotificationException()

    def _retry_notification(
        self,
        max_retries: int,
        user_ids_for_retry: list[int],
    ) -> None:
        """
        Попытка повторного оповещения пользователей.

        :param max_retries:
        :type max_retries: int
        :param user_ids_for_retry: ID не оповещенных пользователей.
        :type user_ids_for_retry: list[int]

        :return:
        :rtype: None
        """
        try:
            if (
                kwargs := self.request.kwargs
            ) and (
                max_retries - self.request.retries
            ):
                kwargs["to_user_ids"] = user_ids_for_retry
                logger.info(
                    "[*] Notification task was retry for UserIDs: "
                    f"{user_ids_for_retry}"
                )

                raise self.retry(
                    countdown=15,
                    max_retries=max_retries,
                    kwargs=kwargs
                )

        except MaxRetriesExceededError:
            pass

        logger.warning(
            f"[!] Limit by max retries, UserIDs {user_ids_for_retry}"
            " not notify..."
        )

    @staticmethod
    def _notification_by_email(user: User, message: str) -> str:
        status = NotificationStatusEnum.success.name

        try:
            notifier = EmailNotifier(user, message)
            notifier.notify()

            logger.info(f"[*] Send email to '{user.username}' was success...")

        except EmailNotificationError as ex:
            status = NotificationStatusEnum.error.name
            logger.error(f"[!] Error send email to '{user.username}': {ex}")

        return status

    @staticmethod
    def _notification_by_sms(user: User, message: str) -> str:
        status = NotificationStatusEnum.success.name

        try:
            notifier = SMSNotifier(user, message)
            notifier.notify()

            logger.info(f"[*] Send sms to '{user.username}' was success...")

        except SMSNotificationError as ex:
            status = NotificationStatusEnum.error.name
            logger.error(f"[!] Error send sms to '{user.username}': {ex}")

        return status

    @staticmethod
    def _notification_by_tg(user: User, message: str) -> str:
        status = NotificationStatusEnum.success.name

        try:
            notifier = TelegramNotifier(user, message)
            notifier.notify()

            logger.info(
                f"[*] Send telegram message to '{user.username}' was "
                "success..."
            )

        except TelegramNotificationError as ex:
            status = NotificationStatusEnum.error.name
            logger.error(
                f"[!] Error send telegram message to '{user.username}': {ex}"
            )

        return status


send_notification = app.task(
    bind=True,
    base=SendNotificationTask
)(
    SendNotificationTask.run
)
