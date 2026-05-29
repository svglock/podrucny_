from django.conf import settings
from django.db import models
from orders.models import Order


class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = (
        ('pending', 'Создана'),
        ('on_way', 'Выехал'),
        ('at_client', 'У клиента'),
        ('returned', 'Возврат'),
        ('completed', 'Завершён'),
    )
    route_duration_minutes = models.IntegerField(
        default=0
    )
    start_address = models.CharField(
        max_length=255,
        blank=True
    )

    end_address = models.CharField(
        max_length=255,
        blank=True
    )

    route_geometry = models.JSONField(
        null=True,
        blank=True
    )
    distance_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    delivery_status = models.CharField(
        max_length=30,
        choices=DELIVERY_STATUS_CHOICES,
        default='pending'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery'
    )
    courier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries'
    )
    address = models.CharField(
        max_length=255,
        default='Unknown address'
    )
    comment = models.TextField(blank=True, null=True)
    estimated_time = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_delivery_price(self):
        if self.order.total_price >= 10000:
            return 0
        return self.distance_km * 15

    def __str__(self):
        return f'Delivery #{self.id}'

    def save(self, *args, **kwargs):
        self.delivery_price = self.calculate_delivery_price()
        super().save(*args, **kwargs)
