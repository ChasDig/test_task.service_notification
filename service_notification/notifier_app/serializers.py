from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User
from .utils.custom_enums import NotificationTypeEnum


class NotificationSerializer(serializers.Serializer):
    """Serializer - оповещение Пользователя."""

    @staticmethod
    def validate_types(value: list[str]) -> list[str]:
        """
        Проверка корректности указанных типов оповещения.

        :param value:
        :type value: list[str]

        :return:
        :rtype: list[str]
        """
        if ex_types := (
            set(value).difference(set(NotificationTypeEnum.values()))
        ):
            raise serializers.ValidationError(
                f"Указанные типы оповещений не найдены: {', '.join(ex_types)}"
            )

        return value

    @staticmethod
    def check_users_exist(value: list[int]) -> list[int]:
        """
        Проверка существования пользователей.

        :param value:
        :type value: list[int]

        :return:
        :rtype: list[int]
        """
        found_ids = (
            User.objects.filter(
                id__in=value
            ).values_list(
                "id",
                flat=True,
            )
        )

        if not_found_ids := set(value) - set(found_ids):
            raise serializers.ValidationError(
                f"Пользователи не найдены: {not_found_ids}"
            )

        return value

    to_user_ids = serializers.ListField(
        validators=[
            check_users_exist,
        ],
        child=serializers.IntegerField(),
        help_text="ID пользователей",
        min_length=1,
        max_length=50,
    )
    types = serializers.ListField(
        validators=[
            validate_types,
        ],
        help_text="Массив типов(источников) оповещений",
    )
    message = serializers.CharField(help_text="Сообщение")
    use_other_types_on_error = serializers.BooleanField(
        default=True,
        help_text=(
            "Флаг - использовать типы, не указанные в поле 'types', если "
            "указанные источники не отправят оповещение по причине ошибки"
        ),
    )
    max_retries = serializers.IntegerField(
        max_value=3,
        min_value=0,
        default=0,
        help_text=(
            "Максимальное кол-во 'retry' задачи по оповещению, в случае если "
            "оповещение по не указанным источникам не сработает"
        ),
    )
