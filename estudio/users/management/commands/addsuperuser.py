from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands.createsuperuser import Command as DjangoCommand
from django.db import transaction


class Command(DjangoCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        # I'd like to add a password.
        parser.add_argument(
            "--password", dest="password", help="Specifies the password for the superuser."
        )
        # Specify the user's primary key.
        parser.add_argument("--pk", dest="pk", help="Specifies the primary key for the superuser.")
        parser.add_argument("--first-name")
        parser.add_argument("--last-name")

    def handle(self, *args, **options):
        super().handle(*args, **options)
        username = options.get("username")
        password = options.get("password")
        first_name = options.get("first_name")
        last_name = options.get("last_name")
        pk = options.get("pk")
        model = get_user_model()
        user = model.objects.get(username=username)
        with transaction.atomic():
            if pk:
                # Delete previous user with random pk
                user.delete()
                user.pk = pk
            if password:
                user.set_password(password)
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()
