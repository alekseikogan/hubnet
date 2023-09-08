from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path
from django.urls import reverse_lazy
from .views import SignUp

app_name = 'users'

urlpatterns = [
    # вход
    path(
      'login/',
      LoginView.as_view(template_name='users/login.html'),
      name='login'
    ),
    # выход
    path(
      'logout/',
      LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    path(
      'signup/',
      SignUp.as_view(template_name='users/signup.html'),
      name='signup'
    ),
    # смена пароля (тупит)
    path(
      'password_change/',
      PasswordChangeView.as_view(
        template_name='users/password_change_form.html',
        success_url=reverse_lazy('password_change_done')),
      name='password_change_form'
    ),
    # успешная смена пароля
    path(
      'password_change/done/',
      PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
      name='password_change_done'
    ),
    # сброс пароля
    path(
      'password_reset/',
      PasswordResetView.as_view(
          template_name='users/password_reset_form.html'),
      name='password_reset_form'
    ),
    # ссылка на почту отправлена
    path(
      'password_reset/done/',
      PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
      name='password_reset_done'
    ),
    # сброс пароля через почту
    path(
      'reset/<uidb64>/<token>/',
      PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
      name='password_reset_confirm'
    ),
    # успешный сброс пароля
    path(
      'reset/done/',
      PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
      name='password_reset_complete'
    ),
   
]
