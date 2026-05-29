from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ProductViewSet, OrderViewSet, api_root, DeliveryViewSet, DashboardAPIView, AlertsAPIView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'deliveries', DeliveryViewSet, basename='delivery')

urlpatterns = [
    path('', api_root),
    path('alerts/', AlertsAPIView.as_view()),
    path('dashboard/', DashboardAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
urlpatterns += router.urls
