from warehouse.models import Product
from orders.models import Order


def get_low_stock_products():

    return Product.objects.filter(
        quantity__lt=10
    )


def get_new_orders():

    return Order.objects.filter(
        status='new'
    )