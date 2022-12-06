from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django import forms
from .forms import RegisterForm, UserUpdateForm, ChangePasswordForm, ProfileUpdateForm
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django.contrib.auth.decorators import login_required


class UserRegistration(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

   



class ChangePassword(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'registration/change_password.html' 
    success_url = reverse_lazy('home')


# class ProfileView(DetailView):
#     model = Profile
#     template_name = 'registration/user_profile.html'

#     def get_context_data(self, **kwargs):
#         # users = Profile.objects.all()
#         context = super(Profile, self).get_context_data(**kwargs)
#         blog_user = get_object_or_404(Profile, self.kwargs['pk'])
#         context['blog_user'] = blog_user
#         return context


# class UserUpdate(generic.UpdateView):
#     form_class = UserUpdateForm
#     template_name = 'registration/edit_userprofile.html'
#     success_url = reverse_lazy('home')

#     def get_object(self):
#         return self.request.user


@login_required
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'registration/edit_userprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })