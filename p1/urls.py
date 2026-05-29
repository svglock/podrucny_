from django.urls import path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ProductViewSet,
    OrderViewSet,
)

router = DefaultRouter()

router.register(
    r'products',
    ProductViewSet,
    basename='product',
)

router.register(
    r'orders',
    OrderViewSet,
    basename='order',
)

urlpatterns = [

    path(
        'token/',
        TokenObtainPairView.as_view(),
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
    ),
]

urlpatterns += router.urls