from django.db import models
from django.urls.base import reverse


class Categories(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name="URL",
    )

    class Meta:
        db_table = "Category"
        verbose_name = "Категрію"
        verbose_name_plural = "Категорії"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Назва")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name="URL",
    )

    description = models.TextField(null=True, blank=True, verbose_name="Опис")
    image = models.ImageField(
        upload_to="goods_images", null=True, blank=True, verbose_name="Зображення"
    )
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Ціна"
    )
    discount = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2, verbose_name="Знижка у %"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість товару")
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)

    class Meta:
        db_table = "product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} - Кількість {self.quantity} - Ціна {self.price}"

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    def product_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount) / 100, 2)

        return self.price
