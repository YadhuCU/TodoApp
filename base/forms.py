from django.forms import ModelForm
from .models import Task, User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']