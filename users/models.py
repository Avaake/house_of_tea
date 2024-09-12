from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(
        upload_to="users_image",
        null=True,
        blank=True,
        verbose_name="Аватар",
    )

    class Meta:
        db_table = "user"
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.username
