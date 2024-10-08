from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

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


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, f"Оновлено")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, f"Виникла помилка")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HoT - Мій профіль"
        context["orders"] = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
        return context


class UsersCartView(TemplateView):
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HoT - Кошик"
        return context
