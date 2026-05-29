from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'courier',
        'delivery_status',
        'delivery_price',
        'created_at',
    )

    list_filter = (
        'delivery_status',
    )

    search_fields = (
        'order__id',
        'courier__username',
    )