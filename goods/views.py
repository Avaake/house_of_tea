from django.shortcuts import render


def catalog(request):
    return render(
        request=request,
        template_name="goods/catalog.html",
    )


def product(request):
    return render(
        request=request,
        template_name="goods/product.html",
    )
