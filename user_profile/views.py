from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django import forms
from .forms import RegisterForm, UserUpdateForm, ChangePasswordForm
from django.utils.translation import gettext_lazy as _
from .models import Profile


class UserRegistration(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

   

class UserUpdate(generic.UpdateView):
    form_class = UserUpdateForm
    template_name = 'registration/edit_userprofile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class ChangePassword(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('home')


class ProfileView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

