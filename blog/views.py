from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
# def home(request):
#     return render(request, 'home.html', {})


class Home(ListView):
    model = BlogPost
    template_name = 'home.html'


class BlogDetail(DetailView):
    model = BlogPost
    template_name = 'blog_details.html'