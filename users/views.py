from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users.forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(
                username=username,
                password=password,
            )

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вас було авторизовано.")

                redirect_page = request.POST.get("next", None)
                print(redirect_page)
                if redirect_page and redirect_page != reverse("users:login"):
                    return HttpResponseRedirect(request.POST.get("next", None))

                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()

    context = {
        "title": "Авторизація",
        "form": form,
    }

    return render(
        request,
        "users/login.html",
        context,
    )


def registration(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)

            messages.success(
                request,
                f"{user.username}, Ви успішно зареєструвалися та авторизовано на сайты.",
            )

            return HttpResponseRedirect(reverse("main:index"))

    else:
        form = UserRegisterForm()

    context = {
        "title": "Реестрація",
        "form": form,
    }
    return render(
        request,
        "users/registration.html",
        context,
    )


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST,
            instance=request.user,
            files=request.FILES,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Оновлено",
            )
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        "title": "Мій профіль",
        "form": form,
    }
    return render(
        request=request,
        template_name="users/profile.html",
        context=context,
    )


def users_cart(request):
    context = {
        "title": "Кошик",
    }
    return render(
        request=request,
        template_name="users/users_cart.html",
        context=context,
    )


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Всього гарного.")
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
