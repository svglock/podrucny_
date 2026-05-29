from django.contrib import admin

from .models import (
    Invoice,
    CommercialOffer,
    ShippingDocument
)

admin.site.register(Invoice)
admin.site.register(CommercialOffer)
admin.site.register(ShippingDocument)