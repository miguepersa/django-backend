from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your views here.

from config.settings.base import EMAIL_HOST_USER


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    context = {
        'user': f"{reset_password_token.user.first_name} {reset_password_token.user.last_name}",
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        'reset_url': f"{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}"
    }

    template = 'mailer/user_reset_password.html'
    email_plaintext_message = render_to_string(template, context)

    send_mail(
        # title:
        "Recuperacion de contraseña - Plataforma Kurios",
        # message:
        '',
        # from:
        EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
        False,
        html_message=email_plaintext_message

    )

# Metodo para enviar contrasenas por primera vez
