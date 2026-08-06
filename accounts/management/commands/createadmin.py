from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Creates an admin user if it doesn't exist."

    def handle(self, *args, **kwargs):

        username = "admin"
        email = "admin@example.com"
        password = "Admin@123"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Admin already exists."))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("Superuser created successfully."))