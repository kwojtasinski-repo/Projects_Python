import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create initial admin user if it does not exist"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write(self.style.WARNING("Admin credentials not provided – skipping"))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("Admin user already exists")
            return

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )

        self.stdout.write(self.style.SUCCESS("Admin user created"))
