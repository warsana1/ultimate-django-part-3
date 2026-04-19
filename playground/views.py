from django.core.mail import EmailMessage, BadHeaderError, mail_admins
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        email = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Mosh'},
        )
        email.send(['to@warsana.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
