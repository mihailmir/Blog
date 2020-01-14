from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .tasks import send_mail


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    model = User
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        send_mail.apply_async(args=[form.cleaned_data.get('username'), form.cleaned_data.get('email')])
        return super().form_valid(form)
