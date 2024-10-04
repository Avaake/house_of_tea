from django.views.generic import ListView, DetailView

from goods.models import Products
from goods.utils import q_search
from django.http import Http404


class CatalogView(ListView):
    model = Products
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 3

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale", None)
        order_by = self.request.GET.get("order_by", None)
        min_range = self.request.GET.get("minRange", 1)
        max_range = self.request.GET.get("maxRange", 1000)
        query = self.request.GET.get("q", None)

        if category_slug == "all":
            goods = super().get_queryset().order_by("id")
        elif query or query == "":
            goods = q_search(query)
        else:
            goods = (
                super()
                .get_queryset()
                .filter(category__slug=category_slug)
                .filter(price__gte=min_range, price__lte=max_range)
            )
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)
        if order_by and order_by != "default":
            goods = goods.order_by(order_by)
        if not isinstance(goods, list):
            goods = goods.filter(price__gte=min_range, price__lte=max_range)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HoT - Каталог"
        context["slug_url"] = self.kwargs.get("category_slug")
        return context


class ProductView(DetailView):
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context
