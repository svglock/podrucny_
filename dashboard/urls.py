from django.urls import path

from . import views
from .views import (
    login_view,
    logout_view,
    dashboard_view,
    products_view,
    orders_view,
    deliveries_view,
    documents_view,
    change_order_status,
    invoice_pdf,
    create_order_view,
    import_excel_view,
    import_xml_view,
    change_delivery_status,
    create_delivery_view,
    shipping_pdf,
    export_orders_excel,
    stock_movements_view,
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('products/', products_view, name='products'),
    path('products/import/', import_excel_view, name='import_excel'),
    path('products/import-xml/', import_xml_view, name='import_xml'),
    path('orders/', orders_view, name='orders'),
    path('orders/create/', create_order_view, name='create_order'),
    path('orders/<int:order_id>/<str:status>/', change_order_status, name='change_order_status'),
    path('deliveries/', deliveries_view, name='deliveries'),
    path('deliveries/create/', create_delivery_view, name='create_delivery'),
    path('deliveries/<int:delivery_id>/<str:status>/', change_delivery_status, name='change_delivery_status'),
    path('documents/', documents_view, name='documents'),
    path('invoice/<int:invoice_id>/pdf/', invoice_pdf, name='invoice_pdf'),
    path('profile/', views.profile_view, name='profile'),
    path('shipping/<int:shipping_id>/pdf/', shipping_pdf, name='shipping_pdf'),
    path('orders/export/', export_orders_excel, name='export_orders'),
    path('stock-movements/', stock_movements_view, name='stock_movements'),
    path('documents/shipping/<int:order_id>/', views.shipping_document_view, name='shipping_document'),
]
