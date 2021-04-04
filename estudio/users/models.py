import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    is_student = models.BooleanField(verbose_name="user is a student", default=False)
    is_teacher = models.BooleanField(verbose_name="user is a teacher", default=False)

    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        blank=False,
        null=False,
        default="example@example.com",
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username
