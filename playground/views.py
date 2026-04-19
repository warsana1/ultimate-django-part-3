from django.core.mail import EmailMessage, BadHeaderError, mail_admins
from django.shortcuts import render


def say_hello(request):
    try:
        message = EmailMessage(
            'Hello from Django',
            'This is a test email sent from a Django view.', 'from@warsana.com', ['to@warsana.com'])
        message.attach_file('playground/static/images/me.jpeg')
        message.send()
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
