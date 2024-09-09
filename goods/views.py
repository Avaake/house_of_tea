from django.shortcuts import render
from goods.models import Products


def catalog(request):

    goods = Products.objects.all()

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
