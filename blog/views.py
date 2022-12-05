from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
# def home(request):
#     return render(request, 'home.html', {})
from .forms import BlogPostForm

class Home(ListView):
    model = BlogPost
    template_name = 'home.html'


class BlogDetail(DetailView):
    model = BlogPost
    template_name = 'blog_details.html'


class CreateBlog(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'add_blogpost.html'


class EditBlog(UpdateView):
    model = BlogPost
    template_name = 'edit_blog.html'
    fields = ('title', 'title_tag', 'body')
    