from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
# Create your views here.


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    model = User
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('articles')
