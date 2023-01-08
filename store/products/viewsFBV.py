# from django.core.paginator import Paginator
# from django.shortcuts import render
#
# from .models import Product, ProductCategory
#
#
# def index(request):
#     context = {'title': 'Store'}
#     return render(request, 'products/index.html', context)
#
#
# def products(request, category_id=None, page_number=1):
#     title = 'Store - Каталог'
#     products = (
#         Product.objects.filter(category_id=category_id)
#         if category_id
#         else Product.objects.all()
#     )
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#     categories = ProductCategory.objects.all()
#     context = {
#         'title': title,
#         'categories': categories,
#         'products': products_paginator,
#         'category_id': category_id
#     }
#     return render(request, 'products/products.html', context)
