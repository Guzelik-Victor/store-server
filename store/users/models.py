from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    email = models.EmailField('email address', unique=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    # формирует уникальный код
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        # формируем ссылку по которой пользователь должен перейти
        link = reverse(
            'users:verify_email',
            kwargs={'email': self.user.email, 'code': self.code}
        )
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи перейдите по ссылку: {}'\
            .format(
                verification_link
            )
        # отправляем сообщение с сформированной ссылкой,
        # перейдя по ней, отработает контроллер
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        # проверят текущее время с утановленным сроком действия кода
        return now() >= self.expiration
