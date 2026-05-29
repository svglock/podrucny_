import uuid

from django.db import models
from orders.models import Order


class Invoice(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )
    payment_status = models.CharField(
        max_length=30,
        default='pending'
    )

    payment_url = models.URLField(
        blank=True
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    number = models.CharField(
        max_length=50,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.number


class CommercialOffer(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    comment = models.TextField(
        blank=True
    )

    def __str__(self):
        return f'Offer {self.id}'


class ShippingDocument(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    number = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    sender_company = models.CharField(
        max_length=255,
        default='ООО "СИНХРА"'
    )

    recipient_company = models.ForeignKey(
        'orders.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shipping_documents'
    )

    route = models.CharField(
        max_length=255
    )

    vehicle_number = models.CharField(
        max_length=50,
        blank=True
    )

    driver_name = models.CharField(
        max_length=255,
        blank=True
    )

    cargo_description = models.TextField(
        blank=True
    )

    cargo_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    places_count = models.IntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'ТН #{self.number}'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f'TH-{uuid.uuid4().hex[:8].upper()}'

        super().save(*args, **kwargs)


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def create_order_documents(sender, instance, created, **kwargs):
    if created:
        # Собираем описание груза из всех позиций заказа
        items = instance.items.all()
        cargo_desc = ', '.join(
            [f'{item.product.title} ({item.quantity} шт.)' for item in items]
        ) if items.exists() else 'Груз не указан'

        # Суммарный вес – можно рассчитать, но сейчас заглушка
        total_weight = sum(
            item.product.weight if hasattr(item.product, 'weight') and item.product.weight else 1
            for item in items
        ) if items.exists() else 10.0

        Invoice.objects.get_or_create(
            order=instance,
            defaults={
                'number': str(
                    uuid.uuid4()
                )[:8],
                'total_amount': instance.total_price,
                'payment_url': f'https://pay.syncra.ru/invoice/{instance.id}/'
            }
        )

        CommercialOffer.objects.get_or_create(
            order=instance
        )

        ShippingDocument.objects.get_or_create(
            order=instance,
            defaults={
                'route': 'Не назначен',
                'recipient_company': instance.customer_company,
                'cargo_description': cargo_desc,
                'cargo_weight': total_weight,
                'places_count': items.count() if items.exists() else 1
            }
        )
