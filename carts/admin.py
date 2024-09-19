from django.contrib import admin
from carts.models import Cart

# admin.site.register(Cart)


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ("product", "quantity", "create_timestamp")
    search_fields = ("product", "quantity", "create_timestamp")
    readonly_fields = ("create_timestamp",)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user_display", "product_display", "quantity", "create_timestamp")
    list_filter = (
        "create_timestamp",
        "product__name",
    )

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимний пользователь"

    def product_display(self, obj):
        return str(obj.product.name)
