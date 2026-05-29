from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from warehouse.models import Product


class Company(models.Model):
    name = models.CharField(
        max_length=255
    )

    inn = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\d+$'
            )
        ]
    )

    kpp = models.CharField(
        max_length=9,
        blank=True
    )

    address = models.TextField()

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('assembly', 'В сборке'),
        ('shipped', 'Отгружен'),
        ('delivering', 'Доставляется'),
        ('delivered', 'Доставлен'),
        ('closed', 'Закрыт'),
        ('cancelled', 'Отменён'),
    )
    MIN_ORDER_AMOUNT = 1000
    customer_company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    manager_comment = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_orders'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f'{self.product.title} x {self.quantity}'
