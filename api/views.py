from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum
from django.utils import timezone
from warehouse.models import Product
from orders.models import Order
from logistics.models import Delivery
from inventory.models import StockMovement
from .serializers import (
    ProductSerializer,
    OrderSerializer,
    DeliverySerializer,
)
from .services import (
    get_low_stock_products,
    get_new_orders,
)
from .permissions import (
    IsSupplier,
    IsCustomer,
    IsCourier,
    IsManager,
    IsOwnerOrManager,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        'supplier',
    ]

    search_fields = [
        'title',
        'description',
    ]

    ordering_fields = [
        'price',
        'quantity',
        'created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'supplier':
            return Product.objects.filter(supplier=user).order_by('-created_at')
        return Product.objects.all().order_by('-created_at')


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'customer']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        if user.role in ['manager', 'admin']:
            return Order.objects.all()
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status != 'new':
            return Response({'error': 'Подтвердить можно только новый заказ'}, status=400)

        for item in order.items.all():
            product = item.product
            product.reserved_quantity -= item.quantity
            product.quantity -= item.quantity
            product.save()

            StockMovement.objects.create(
                product=product,
                movement_type='writeoff',
                quantity=item.quantity,
                comment=f'Списание по заказу #{order.id}',
                created_by=request.user,
            )

        order.status = 'confirmed'
        order.save()
        return Response({'status': 'Заказ подтверждён'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != 'new':
            return Response({'error': 'Отменить можно только новый заказ'}, status=400)

        for item in order.items.all():
            product = item.product
            product.reserved_quantity -= item.quantity
            product.save()

            StockMovement.objects.create(
                product=product,
                movement_type='return',
                quantity=item.quantity,
                comment=f'Снятие резерва заказа #{order.id}',
                created_by=request.user,
            )

        order.status = 'cancelled'
        order.save()
        return Response({'status': 'Заказ отменён'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['confirmed', 'assembly', 'shipped', 'delivering']:
            return Response({'error': 'Заказ нельзя завершить в текущем статусе'}, status=400)
        order.status = 'delivered'  # или 'closed', если нужен отдельный шаг
        order.save()
        return Response({'status': 'Заказ доставлен'})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        order = self.get_object()
        if request.user.role not in ['manager', 'admin']:
            raise PermissionDenied('Только manager может подтверждать заказы')
        if order.status != 'new':
            return Response({'error': 'Заказ уже обработан'}, status=400)
        order.status = 'confirmed'
        order.approved_by = request.user
        order.approved_at = timezone.now()
        manager_comment = request.data.get('manager_comment')
        if manager_comment:
            order.manager_comment = manager_comment
        order.save()
        return Response({'status': 'Заказ подтвержден'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        order = self.get_object()
        if request.user.role not in ['manager', 'admin']:
            raise PermissionDenied('Только manager может отклонять заказы')
        if order.status != 'new':
            return Response({'error': 'Заказ уже обработан'}, status=400)
        order.status = 'cancelled'
        manager_comment = request.data.get('manager_comment')
        if manager_comment:
            order.manager_comment = manager_comment
        order.save()
        return Response({'status': 'Заказ отклонен'})


class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['manager', 'admin'] or user.is_staff:
            return Delivery.objects.all().order_by('-created_at')
        if user.role == 'courier':
            return Delivery.objects.filter(courier=user).order_by('-created_at')
        return Delivery.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role not in ['manager', 'admin']:
            raise PermissionDenied('Только manager может создавать delivery')
        serializer.save()

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):

        delivery = self.get_object()

        delivery.delivery_status = 'on_way'
        delivery.save()

        return Response({
            'status': 'Выехал'
        })

    @action(detail=True, methods=['post'])
    def arrive(self, request, pk=None):

        delivery = self.get_object()

        delivery.delivery_status = 'at_client'
        delivery.save()

        return Response({
            'status': 'У клиента'
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):

        delivery = self.get_object()

        delivery.delivery_status = 'completed'

        delivery.save()

        return Response({
            'status': 'Доставка завершена'
        })

    @action(detail=True, methods=['post'])
    def return_delivery(self, request, pk=None):

        delivery = self.get_object()

        delivery.delivery_status = 'returned'

        delivery.save()

        return Response({
            'status': 'Возврат'
        })


@api_view(['GET'])
def api_root(request):
    return Response({
        'products': '/api/v1/products/',
        'orders': '/api/v1/orders/',
        'deliveries': '/api/v1/deliveries/',
        'token': '/api/v1/token/',
        'docs': '/api/docs/',
        'admin': '/admin/',
    })


class DashboardAPIView(APIView):
    def get(self, request):
        total_orders = Order.objects.count()
        new_orders = Order.objects.filter(status='new').count()
        confirmed_orders = Order.objects.filter(status='confirmed').count()
        delivered_orders = Order.objects.filter(status='delivered').count()
        total_products = Product.objects.count()
        total_stock = Product.objects.aggregate(total=Sum('quantity'))['total'] or 0
        revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

        return Response({
            'total_orders': total_orders,
            'new_orders': new_orders,
            'confirmed_orders': confirmed_orders,
            'delivered_orders': delivered_orders,
            'total_products': total_products,
            'total_stock': total_stock,
            'revenue': revenue,
        })


class AlertsAPIView(APIView):
    def get(self, request):
        low_stock = get_low_stock_products()
        new_orders = get_new_orders()

        return Response({
            'low_stock_products': [
                {'id': p.id, 'title': p.title, 'quantity': p.quantity}
                for p in low_stock
            ],
            'new_orders': [
                {'id': o.id, 'customer': o.customer.username, 'total_price': o.total_price}
                for o in new_orders
            ]
        })
