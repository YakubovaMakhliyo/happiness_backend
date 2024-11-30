from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from scr.user.views import *

urlpatterns = [
    path('register', UserRegisterCreateAPIView.as_view()),
    path('activate-code', CheckActivationCodeGenericAPIView.as_view()),
    path('reset-password', ResetPasswordView.as_view()),
    path('reset-password-confirm', ResetPasswordConfirmView.as_view()),
    path('', UserUpdateView.as_view(), name='user-update'),
    path('login', TokenObtainPairView.as_view()),
    path('login-refresh', TokenRefreshView.as_view()),
    path('update/tg', UsrTgUpdateAPIView.as_view()),
]
