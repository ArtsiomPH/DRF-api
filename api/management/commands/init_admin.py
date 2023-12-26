from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(
        self, *args: tuple[Any, ...], **options: dict[str, Any]
    ) -> None:
        User = get_user_model()
        if User.objects.count() == 0:
            username = "admin"
            password = "admin"
            print(f"Creating account for {username}")
            admin = User.objects.create_superuser(
                username=username, password=password
            )
            admin.is_active = True
            admin.is_admin = True
            admin.role = "admin"
            admin.save()
        else:
            print(
                "Admin accounts can only be initialized if no Accounts exist"
            )
