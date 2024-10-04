from django.shortcuts import render, get_list_or_404
from goods.models import Products
from django.core.paginator import Paginator
from goods.utils import q_search
from django.http import Http404
from django.shortcuts import render


def catalog(request, category_slug=None):
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    min_range = request.GET.get("minRange", 1)
    max_range = request.GET.get("maxRange", 1000)
    query = request.GET.get("q", None)

    print(min_range, max_range)

    if category_slug == "all":
        goods = Products.objects.all().order_by("id")
    elif query or query == "":
        goods = q_search(query)
    else:
        # goods = get_list_or_404(
        #     Products.objects.filter(category__slug=category_slug).filter(
        #         price__gte=min_range, price__lte=max_range
        #     )
        # )
        goods = Products.objects.filter(category__slug=category_slug).filter(
            price__gte=min_range, price__lte=max_range
        )
        if not goods.exists():
            raise Http404()

    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)
    if not isinstance(goods, list):
        goods = goods.filter(price__gte=min_range, price__lte=max_range)

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
