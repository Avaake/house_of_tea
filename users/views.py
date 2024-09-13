from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users.forms import UserLoginForm, UserRegisterForm, ProfileForm


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


def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST,
            instance=request.user,
            files=request.FILES,
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileForm(instance=request.user)

    context = {"totle": "Мій профіль", "form": form}
    return render(
        request=request,
        template_name="users/profile.html",
        context=context,
    )


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("main:index"))
