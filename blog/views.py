from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
# def home(request):
#     return render(request, 'home.html', {})
from .forms import BlogPostForm, EditBlogPostForm

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
    form_class = EditBlogPostForm
    template_name = 'edit_blog.html'
    
    