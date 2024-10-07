from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from carts.models import Cart
from orders.models import Order, OrderItem


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse_lazy("users:login"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_key = Cart.objects.filter(user=user)
                if forgot_key.exists():
                    forgot_key.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(
                    self.request, f"{user.username}, Вас було авторизовано."
                )
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HoT - Авторизація"
        return context


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(
            self.request,
            f"{user.username}, Ви успішно зареєструвалися та авторизовано на сайты.",
        )
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HoT - Реестрація"
        return context


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
            messages.success(request, f"Оновлено")
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileForm(instance=request.user)

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by("-id")
    )

    context = {
        "title": "Мій профіль",
        "form": form,
        "orders": orders,
    }
    return render(
        request=request,
        template_name="users/profile.html",
        context=context,
    )


def users_cart(request):
    return render(request, "users/users_cart.html")


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Всього гарного.")
    auth.logout(request)
    return redirect(reverse("main:index"))
