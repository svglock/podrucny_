from django.conf import settings
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('food', 'Продукты питания'),
        ('drinks', 'Напитки'),
        ('tech', 'Техника'),
        ('other', 'Прочее'),
    )
    discount_percent = models.DecimalField('Скидка (%)', max_digits=5, decimal_places=2, default=0)
    markup_percent = models.DecimalField('Наценка (%)', max_digits=5, decimal_places=2, default=0)
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Поставщик')
    title = models.CharField('Название товара', max_length=255)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Остаток на складе', default=0)
    reserved_quantity = models.PositiveIntegerField('В резерве', default=0)
    category = models.CharField('Категория', max_length=50, choices=CATEGORY_CHOICES, default='other')
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    @property
    def final_price(self):

        price = self.price

        if self.markup_percent:
            price += (
                    price * self.markup_percent / 100
            )

        if self.discount_percent:
            price -= (
                    price * self.discount_percent / 100
            )

        return round(price, 2)

    @property
    def available_quantity(self):
        return (
                self.quantity -
                self.reserved_quantity
        )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
