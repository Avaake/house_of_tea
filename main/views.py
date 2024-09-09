from django.shortcuts import render
from unicodedata import category

from goods.models import Categories


def index(request):
    categories = Categories.objects.all()

    context = {
        "title": "Home - Головна",
        "content": "Магазин чаю House of Tea",
        "categories": categories,
    }

    return render(
        request=request,
        template_name="main/index.html",
        context=context,
    )


def about(request):
    context = {
        "title": "Home - О нас",
        "content": "О Нас",
        "text_on_page": "Тут ти зможеш придбати найкращі чаї Китаю",
    }
    return render(
        request=request,
        template_name="main/about.html",
        context=context,
    )
