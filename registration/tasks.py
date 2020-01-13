from blog import app


@app.task(bind=True, max_retries=5)
def send_mail(self, username, email, **kwargs):
    send_mail(
        'Email Confirmation',
        'Hello {}.'.format(username),
        'from@example.com',
        [email],
        fail_silently=False,
    )
