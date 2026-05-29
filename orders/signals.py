from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from logistics.models import Delivery

@receiver(post_save, sender=Order)
def create_delivery(sender, instance, created, **kwargs):
    if created:
        Delivery.objects.create(
            order=instance,
            address='Не указан'
        )