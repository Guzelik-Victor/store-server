import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from .models import EmailVerification, User


# отправку письма для авторизации вынесели в таску для селери
@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration_date = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(
        code=uuid.uuid4(),
        user=user,
        expiration=expiration_date,
    )
    record.send_verification_email()
