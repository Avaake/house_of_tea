from django.shortcuts import render


def login(request):
    context = {
        "title": "Авторизація",
    }
    return render(
        request,
        "users/login.html",
        context,
    )


def registration(request):
    context = {
        "title": "Реестрація",
    }
    return render(
        request,
        "users/registration.html",
        context,
    )


def profile(request):
    context = {
        "totle": "Мій профіль",
    }
    return render(request=request, template_name="users/profile.html", context=context)

def logout(request):
    pass
