from rest_framework import serializers
from warehouse.models import Product
from orders.models import Order, OrderItem
from logistics.models import Delivery
from inventory.models import StockMovement
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    supplier_username = serializers.CharField(
        source='supplier.username', read_only=True
    )
    final_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'supplier', 'supplier_username',
            'title', 'description', 'price', 'quantity', 'created_at', 'discount_percent',
            'markup_percent',
            'final_price',
        ]
        read_only_fields = ['supplier', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'price']
        read_only_fields = ['price']  # цена вычисляется автоматически


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)  # только для записи

    customer_username = serializers.CharField(
        source='customer.username', read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_username', 'status',
            'total_price', 'created_at', 'items', 'manager_comment',
            'approved_by', 'approved_by_username', 'approved_at',
        ]
        read_only_fields = ['customer', 'status', 'total_price', 'created_at', 'approved_by',
                            'approved_at', ]

    approved_by_username = serializers.CharField(
        source='approved_by.username',
        read_only=True
    )

    @transaction.atomic
    def create(self, validated_data):

        items_data = validated_data.pop('items')

        order = Order.objects.create(**validated_data)

        total_price = 0

        for item_data in items_data:

            product = item_data['product']
            quantity = item_data['quantity']

            available_quantity = (
                    product.quantity - product.reserved_quantity
            )

            # Проверка доступного остатка
            if available_quantity < quantity:
                raise serializers.ValidationError(
                    f'Недостаточно товара "{product.title}". '
                    f'Доступно: {available_quantity}'
                )

            # Резервируем
            product.reserved_quantity += quantity
            product.save()

            # Складское движение
            StockMovement.objects.create(
                product=product,
                movement_type='reserve',
                quantity=quantity,
                comment=f'Резерв под заказ #{order.id}',
                created_by=order.customer,
            )

            item_price = (
                    product.final_price * quantity
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item_price,
            )

            total_price += item_price
        if total_price < Order.MIN_ORDER_AMOUNT:
            raise serializers.ValidationError(
                f'Минимальная сумма заказа: {Order.MIN_ORDER_AMOUNT}'
            )
        order.total_price = total_price
        order.save()

        return order


from logistics.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    courier_username = serializers.CharField(
        source='courier.username',
        read_only=True
    )

    class Meta:
        model = Delivery

        fields = [
            'id',
            'order',
            'courier',
            'courier_username',
            'address',
            'comment',
            'delivery_status',
            'estimated_time',
            'delivered_at',
            'created_at',
        ]

        read_only_fields = [
            'status',
            'delivered_at',
            'created_at',
        ]
