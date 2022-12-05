from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost, Topic
from .forms import BlogPostForm, EditBlogPostForm
from django.urls import reverse_lazy

class Home(ListView):
    model = BlogPost
    template_name = 'home.html'
    ordering = ['-creation_date']


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


class DeleteBlog(DeleteView):
    model = BlogPost
    template_name = 'delete_blog.html'
    success_url = reverse_lazy('home')
    

class CreateTopic(CreateView):
    model = Topic
    template_name = 'add_topic.html'
    fields = '__all__'


def topicview(request, item):
    topic_blogposts = BlogPost.objects.filter(topic = item)
    return render(request, 'topics.html', {'item' : item.title(), 'topic_blogposts' : topic_blogposts})