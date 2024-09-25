from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager
from accounts.validators import (
    validate_username,
    validate_name,
    validate_birth_date,
)


class User(AbstractUser):
    username = models.CharField(
        max_length=64, unique=True, validators=[validate_username]
    )
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=64, validators=[validate_name])
    last_name = models.CharField(max_length=64, validators=[validate_name])

    USERNAME_FIELD = "email"
    # Here "email" will be used instead of "username" -> username(=email) and
    # password fields are required by default.
    # Other required fields are listed in the REQUIRED_FIELDS below:
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)


class Profile(models.Model):
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    avatar = models.URLField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(validators=[validate_birth_date])

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        # if not self.avatar:
        #     self.avatar = create_gravatar_url(self.user.email)
        super().save(*args, **kwargs)
