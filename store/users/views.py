from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from products.common.views import TitleMixin
from django.contrib import messages

from django.conf import settings


from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm, UserPasswordResetForm, UserSetPasswordForm
from .models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Подзравляем! Вы успешно зарегистрировались.'
    title = 'Store - Регистрация'


# найти красивое решение, если в адрессной строке набрать чужой id
# как обработать эту ситуацию
# сейчас проверка в шаблоне
class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # переменную baskets определил глобально в контекс процес..
    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        # пользователь переходя по сформированной нами ссылке передает
        # email и uuid code
        code = kwargs['code']
        # достаем юзера по мылу (уникальное поле)
        user = User.objects.get(email=kwargs['email'])
        # из модели получаем нужный объект
        email_verification = EmailVerification.objects.filter(
            user=user,
            code=code
        )
        # если объект существует и код не устарел (2 суток) сохраняем изменения
        # булевая переменная переходит в статус True
        if email_verification.exists()\
                and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(
                EmailVerificationView, self
            ).get(request, *args, **kwargs)
        return redirect(reverse('index'))


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    title = "Store - восстановление пароля"
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_email')
    from_email = settings.EMAIL_HOST_USER


class UserPasswordResetConfirmView(
    SuccessMessageMixin, PasswordResetConfirmView
):
    title = "Store - смена пароля"
    template_name = 'users/password_reset_confirm.html'
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('users:login')
    success_message = 'Ваш пароль был сохранен. Теперь вы можете войти.'


class UserPasswordChange(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/profile.html'
    success_message = 'Ваш пароль изменен'

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, 'Ваш пароль НЕ изменен.<br>'
                                     'При изменении пароля руководствуйтесь инструкцией в форме.')
        return redirect(reverse('users:profile', args=(self.request.user.id,)))

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))












