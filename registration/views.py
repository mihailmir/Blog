from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from .tasks import send_mail


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    model = User
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        send_mail.apply_async(args=[self.request.POST.get('username'), form.cleaned_data.get('email')])
        return redirect(self.success_url)
