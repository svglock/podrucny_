from django.conf import settings
from django.db import models
from warehouse.models import Product


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('income', 'Приход'),
        ('reserve', 'Резерв'),
        ('writeoff', 'Списание'),
        ('return', 'Возврат'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='movements'
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES
    )

    quantity = models.PositiveIntegerField()

    comment = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.title} - {self.movement_type}'
