from django.shortcuts import render, get_list_or_404
from goods.models import Products
from django.core.paginator import Paginator


def catalog(request, category_slug=None):
    page = request.GET.get("page", 1)

    if category_slug == "all":
        goods = Products.objects.all().order_by("id")
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        "title": "Каталог",
        "goods": current_page,
        "slug_url": category_slug,
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
