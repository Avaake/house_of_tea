from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HoT - Головна"
        context["content"] = "Магазин чаю House of Tea"
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HoT - О нас"
        context["content"] = "О нас"
        context["text_on_page"] = "Тут ти зможеш придбати найкращі чаї Китаю"
        return context


# def index(request):
#
#     context = {
#         "title": "Home - Головна",
#         "content": "Магазин чаю House of Tea",
#     }
#
#     return render(
#         request=request,
#         template_name="main/index.html",
#         context=context,
#     )


# def about(request):
#     context = {
#         "title": "Home - О нас",
#         "content": "О Нас",
#         "text_on_page": "Тут ти зможеш придбати найкращі чаї Китаю",
#     }
#     return render(
#         request=request,
#         template_name="main/about.html",
#         context=context,
#     )
