from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django import forms

User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control mb-3'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control mb-3'}))
    # email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        user_exists = User.objects.filter(username=username)
        if user_exists.count():
            raise forms.ValidationError("User with this username already exists, please chose another username.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError(_('Please use another Email, that is already taken'))
        return email
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(_('Passwords do not match.'))
        return cd['password2']



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


#user and profile update forms
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control mb-3'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control mb-3'}))
    class Meta:
        model = User
        fields = ("first_name", "last_name",)


class ProfileUpdateForm(forms.ModelForm):
    # about = forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control mb-3'}))
    class Meta:
        model = Profile
        fields = ("about", "photo",)
        widgets = {
            'about' : forms.Textarea(attrs = {'class':'form-control', 'placeholder': 'Write your story here'}),
            'photo' : forms.FileInput(attrs = {'class': 'form-control'})
        }

#end of user and profile update forms


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control mb-3', 'type' : 'password'}))
    new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control mb-3', 'type' : 'password'}))
    new_password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control mb-3', 'type' : 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
    