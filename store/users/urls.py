from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordResetDoneView
from django.urls import path


from .views import (EmailVerificationView, UserLoginView, UserProfileView,
                    UserRegistrationView, UserPasswordResetView, UserPasswordResetConfirmView, UserPasswordChange)

app_name = 'users'


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path(
        'profile/<int:pk>/',
        login_required(UserProfileView.as_view()),
        name='profile'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'verify/<str:email>/<uuid:code>/',
        EmailVerificationView.as_view(),
        name='verify_email'
    ),
    path(
        'password_reset/',
        UserPasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_email_done.html'
        ),
        name='password_reset_email'
    ),
    path(
        'reset/<uidb64>/<token>/',
        UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password_change',
        UserPasswordChange.as_view(),
        name='password_change'
    ),
]
