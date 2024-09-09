from django.db import models


class Categories(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        max_length=255, unique=True, null=True, blank=True, verbose_name="URL"
    )

    class Meta:
        db_table = "Category"
        verbose_name = "Категрію"
        verbose_name_plural = "Категорії"
        ordering = ["id"]

    def __str__(self):
        return self.name
