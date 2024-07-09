import secrets
import random
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView as LoginBaseView
from django.contrib.auth.views import LogoutView as LogoutBaseView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from users.forms import UserRegisterForm, UserPasswordResetForm
from users.models import User
from config import settings


class LoginView(LoginBaseView):
    template_name = 'users/login.html'


class LogoutView(LogoutBaseView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class PasswordResetView(FormView):
    model = User
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/password_reset.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user.password = make_password(password)
            user.save()

            send_mail(
                subject='Ваш новый пароль',
                message=f'Ваш новый пароль: {password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        return super().form_valid(form)
