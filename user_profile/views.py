from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views import generic
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django import forms
from .forms import RegisterForm, UserUpdateForm, ChangePasswordForm, ProfileUpdateForm
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import BlogPost
from . import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator


User = get_user_model()


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
            messages.success(request, _("Your account details was changed succcessfully!"))
            return redirect('mydashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'registration/edit_userprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def read_later(request, id):
    readlater_blog = get_object_or_404(BlogPost, id = id)
    if readlater_blog.users_readlater.filter(id = request.user.id).exists():
        readlater_blog.users_readlater.remove(request.user)
        messages.success(request, readlater_blog.title + " has been removed from your read later list", extra_tags='readlater')
    else:
        readlater_blog.users_readlater.add(request.user)
        messages.success(request, "Added " + readlater_blog.title + " to your read later list", extra_tags='readlater')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




@login_required
def readlaterview(request):
    # readlater_blogs = BlogPost.objects.filter(users_readlater = request.user)
    paginate = Paginator(BlogPost.objects.filter(users_readlater = request.user), 2)
    page = request.GET.get('page')
    readlaters = paginate.get_page(page)
    nums = "a" * readlaters.paginator.num_pages
    return render(request, 'user_readlater.html', {'readlaters' : readlaters, 'nums' : nums})


 

@login_required
def mydashboard(request):
    return render(request, 'mydashboard.html')

@login_required
def myblogposts(request):
    return render(request, 'myblogs.html')


@login_required
def deleteprofile(request):
    user = models.Profile.objects.get(user=request.user)
    u = User.objects.get(username = request.user)
    user.delete()
    u.delete()
    logout(request)
    return render(request,'registration/delete_confirmation.html')



# def otherprofile(request, id):
#     user = User.objects.get(user = id)
#     # user = get_object_or_404(User, id = id)
#     return render(request, 'other_profile.html', {'user' : user})

class OtherProfile(DetailView):
    model = Profile
    template_name = 'other_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(OtherProfile, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context
    
