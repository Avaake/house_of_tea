from django.shortcuts import render, get_list_or_404
from goods.models import Products


def catalog(request, category_slug=None):

    if category_slug == "all":
        goods = Products.objects.all().order_by("id")
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    context = {
        "title": "Каталог",
        "goods": goods,
    }

    return render(
        request=request,
        template_name="goods/catalog.html",
        context=context,
    )


def product(request, product_slug):
    products = Products.objects.get(slug=product_slug)

    context = {"product": products}

    return render(request=request, template_name="goods/product.html", context=context)
