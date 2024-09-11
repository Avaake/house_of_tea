from goods.models import Products
from django.db.models import Q


def q_search(query):
    # Очистити запит від зайвих пробілів
    query = query.strip()

    # если була передана пуста строка
    if query == "":
        return Products.objects.all().order_by("id")

    # Пошук по ID (якщо запит - це число до 5 символів)
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    # Пошук за ключовими словами в описі та назві
    q_object = Q()
    keywords = [word for word in query.split() if len(word) > 2]

    for token in keywords:
        q_object |= Q(description__icontains=token) | Q(name__icontains=token)

    # Повертаємо результати пошуку
    return Products.objects.filter(q_object).order_by("id")
