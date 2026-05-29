from django.shortcuts import render

from warehouse.models import Product
from .models import StockMovement


def stock_view(request):

    products = Product.objects.all()

    search = request.GET.get('search')

    if search:
        products = products.filter(
            title__icontains=search
        )

    context = {
        'products': products,
        'movements': StockMovement.objects.select_related(
            'product'
        ).order_by('-created_at')[:20]
    }

    return render(
        request,
        'inventory/stock.html',
        context
    )