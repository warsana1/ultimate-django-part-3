from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    try:
        mail_admins("Subject", "Message",
                    html_message="<p>This is an <strong>important</strong> message.</p>")
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
