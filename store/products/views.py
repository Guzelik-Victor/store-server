from django.shortcuts import render

from .models import Product

# Create your views here.


def index(request):
    return render(request, 'products/index.html')


def products(request):
    title = 'Store - Каталог'
    product = Product.objects.all().select_related('category')
    print(product)
    context = {
        'title': title,
        'products': product,

    }
    return render(request, 'products/products.html', context=context)
