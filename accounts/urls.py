from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)
from .views_api import RegisterView, LogoutView

urlpatterns = [
    # Сторінки для людей
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),

    # Верифікація email
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),

    # Скидання пароля (вбудовані Django views)
    path('password-reset/',
     auth_views.PasswordResetView.as_view(
         template_name='accounts/password_reset.html',
         email_template_name='accounts/password_reset_email.html',
         html_email_template_name='accounts/password_reset_email.html',
         subject_template_name='accounts/password_reset_subject.txt',
         success_url='/accounts/password-reset/done/'
     ),
     name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/password-reset/complete/'
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # API (JWT) для майбутнього
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]