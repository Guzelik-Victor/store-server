from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import User
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['title'] = 'Store - Авторизация'
        return context


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['title'] = 'Store - Регистрация'
        return context


# найти красивое решение, если в адрессной строке набрать чужой id
# как обработать эту ситуацию
# сейчас проверка в шаблоне
class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Личный кабинет',
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context
