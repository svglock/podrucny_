import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from documents.models import ShippingDocument
from logistics.models import Delivery
from orders.models import Order, OrderItem, Company
from warehouse.models import Product

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполнение базы реальными данными'

    def handle(self, *args, **kwargs):
        # --- Компании и ИП ---
        companies = [
            Company.objects.get_or_create(
                name='ООО "ТехИмпорт"',
                inn='7701234567', kpp='770101001',
                address='Москва, ул. Тверская, 15',
                email='info@techimport.ru', phone='+7 495 123-45-67'
            )[0],
            Company.objects.get_or_create(
                name='АО "СтройГрад"',
                inn='7809876543', kpp='780201001',
                address='Санкт-Петербург, Невский пр., 100',
                email='office@stroygrad.ru', phone='+7 812 987-65-43'
            )[0],
            Company.objects.get_or_create(
                name='ИП Иванов А.А.',
                inn='501234567890', kpp='',
                address='Екатеринбург, ул. Малышева, 51',
                email='ivanov@mail.ru', phone='+7 343 111-22-33'
            )[0],
            Company.objects.get_or_create(
                name='ООО "ПромСнаб"',
                inn='6312345678', kpp='631201001',
                address='Самара, ул. Гагарина, 22',
                email='promsnab@list.ru', phone='+7 846 555-44-33'
            )[0],
        ]

        # --- Пользователи ---
        manager, _ = User.objects.get_or_create(username='manager', defaults={'role': 'manager', 'is_staff': True})
        manager.set_password('12345678');
        manager.save()

        supplier, _ = User.objects.get_or_create(username='supplier', defaults={'role': 'supplier'})
        supplier.set_password('12345678');
        supplier.save()

        customers = []
        for i in range(3):
            c, _ = User.objects.get_or_create(username=f'customer_{i}', defaults={'role': 'customer'})
            c.set_password('12345678');
            c.save()
            customers.append(c)

        couriers_data = [
            {'username': 'petrov', 'full_name': 'Петров Сергей Викторович'},
            {'username': 'smirnov', 'full_name': 'Смирнов Алексей Иванович'},
            {'username': 'kuznetsova', 'full_name': 'Кузнецова Ольга Петровна'},
        ]
        couriers = []
        for d in couriers_data:
            u, _ = User.objects.get_or_create(username=d['username'], defaults={'role': 'courier'})
            u.set_password('12345678');
            u.save()
            couriers.append(u)

        # --- Товары ---
        product_data = [
            ('Ноутбук Lenovo ThinkPad X1 Carbon', 'tech', 85000, 'Электроника'),
            ('Монитор LG 27GN950-B 27"', 'tech', 35000, 'Электроника'),
            ('Офисное кресло Chairman CH-200', 'other', 12000, 'Мебель'),
            ('Бумага офисная SvetoCopy A4 (500 л.)', 'other', 350, 'Канцелярия'),
            ('Вода питьевая 19 л «Святой источник»', 'food', 200, 'Продукты'),
            ('Картридж лазерный HP 26A (CF226A)', 'tech', 2500, 'Расходники'),
            ('Стол письменный «Стандарт»', 'other', 8000, 'Мебель'),
            ('Чай зелёный Lipton 100 пак.', 'food', 150, 'Продукты'),
            ('Кофе растворимый Jacobs Monarch 500 г', 'food', 600, 'Продукты'),
        ]
        products = []
        for title, cat, price, desc in product_data:
            p, _ = Product.objects.get_or_create(
                title=title,
                defaults={'supplier': supplier, 'price': price, 'quantity': random.randint(10, 100), 'category': cat,
                          'description': desc}
            )
            products.append(p)

        # --- Заказы и доставки ---
        vehicles = ['А123ВС77', 'Е456КХ82', 'М789ОР163', 'Х001ТТ99']
        for idx, company in enumerate(companies):
            customer = random.choice(customers)
            order = Order.objects.create(customer=customer, customer_company=company, status='new', total_price=0)

            # Позиции заказа
            total = 0
            num_items = random.randint(1, 3)
            selected_products = random.sample(products, num_items)
            for product in selected_products:
                qty = random.randint(1, 5)
                price = product.final_price * qty
                OrderItem.objects.create(order=order, product=product, quantity=qty, price=price)
                total += price
            order.total_price = total
            order.save()

            # Доставка
            delivery = order.delivery
            delivery.start_address = 'Москва, ул. Тверская, 15'
            delivery.end_address = company.address
            delivery.distance_km = random.randint(10, 1500)
            delivery.route_duration_minutes = random.randint(30, 600)
            delivery.courier = random.choice(couriers)
            delivery.driver_name = next(u for u in couriers_data if u['username'] == delivery.courier.username)[
                'full_name']
            delivery.vehicle_number = random.choice(vehicles)
            delivery.save()

            # Транспортная накладная
            shipping = ShippingDocument.objects.get(order=order)
            shipping.sender_company = 'ООО "СИНХРА"'
            shipping.recipient_company = company
            shipping.route = f'{delivery.start_address} → {delivery.end_address}'
            shipping.vehicle_number = delivery.vehicle_number
            shipping.driver_name = delivery.driver_name
            shipping.cargo_description = ', '.join(
                [f'{item.product.title} ({item.quantity} шт.)' for item in order.items.all()])
            shipping.cargo_weight = sum(
                item.product.weight if hasattr(item.product, 'weight') and item.product.weight else 1 for item in
                order.items.all()) or 15.0
            shipping.places_count = order.items.count()
            shipping.save()

        self.stdout.write(self.style.SUCCESS('База заполнена реальными данными!'))
