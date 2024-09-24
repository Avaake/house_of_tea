from django.shortcuts import render


def create_order(request):
    context = {
        "title": "Створити замовлення",
    }
    return render(
        request=request,
        template_name="orders/create_order.html",
        context=context,
    )
