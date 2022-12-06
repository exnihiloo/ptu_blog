from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control mb-3'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control mb-3'}))
    # email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'Username'})
            self.fields['email'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
            self.fields['password1'].widget.attrs.update(
                {'class': 'form-control mb-3', 'placeholder': 'Password'})
            self.fields['password2'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Repeat Password'})