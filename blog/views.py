from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost, Topic
from django.views.generic.edit import FormMixin
from .forms import BlogPostForm, EditBlogPostForm, CommentForm
from django.urls import reverse_lazy, reverse

class Home(ListView):
    model = BlogPost
    template_name = 'home.html'
    ordering = ['-creation_date']


    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(Home, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context


class BlogDetail(FormMixin, DetailView):
    model = BlogPost
    template_name = 'blog_details.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blogview', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        form.instance.blogpost = self.get_object()
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'blogpost' : self.get_object(),
            'user' : self.request.user
        }


    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(BlogDetail, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context




class CreateBlog(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'add_blogpost.html'

    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(CreateBlog, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context


class EditBlog(UpdateView):
    model = BlogPost
    form_class = EditBlogPostForm
    template_name = 'edit_blog.html'

    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(EditBlog, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context


class DeleteBlog(DeleteView):
    model = BlogPost
    template_name = 'delete_blog.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(DeleteBlog, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context
    

class CreateTopic(CreateView):
    model = Topic
    template_name = 'add_topic.html'
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(CreateTopic, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context


def topicview(request, item):
    topic = get_object_or_404(Topic, name = item)
    topic_blogposts = BlogPost.objects.filter(topic = topic)
    return render(request, 'topics.html', {'topic' : topic, 'topic_blogposts' : topic_blogposts})


