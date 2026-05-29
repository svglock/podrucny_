from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'supplier',
        'price',
        'quantity',
        'category',
        'created_at',
    )

    list_filter = (
        'category',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
    )