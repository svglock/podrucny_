from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('manager', 'Менеджер'),
        ('warehouse', 'Склад'),
        ('logistician', 'Логист'),
        ('driver', 'Водитель'),
        ('admin', 'Администратор'),
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='manager'
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    company_name = models.CharField(
        max_length=255,
        blank=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"