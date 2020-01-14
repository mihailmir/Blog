from blog import app
from django.core.mail import send_mail as sd


@app.task(bind=True, max_retries=5)
def send_mail(self, username, email, **kwargs):
    sd(
        'Email Confirmation',
        'Hello {}.'.format(username),
        'from@example.com',
        [email],
        fail_silently=False,
    )
