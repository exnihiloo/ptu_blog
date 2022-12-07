from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost, Topic, BlogLike
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from .forms import BlogPostForm, EditBlogPostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

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



def search(request):
    query = request.GET.get('query')
    search_results = BlogPost.objects.filter(Q(title__icontains=query) | 
        Q(author__username__icontains=query) | 
        Q(topic__name__icontains=query) 
    )
    return render(request, 'search.html', {'blogposts': search_results, 'query': query})

@login_required
def likes(request, pk):
    user = request.user
    blogpost = BlogPost.objects.get(id = pk)
    current_likes = blogpost.likes
    liked = BlogLike.objects.filter(user = user, liked_blog = blogpost).count()
    if not liked:
        liked = BlogLike.objects.create(user = user, liked_blog = blogpost)
        current_likes += 1
    else:
        liked = BlogLike.objects.filter(user = user, liked_blog = blogpost).delete()
        current_likes -= 1
    blogpost.likes = current_likes
    blogpost.save()
    return HttpResponseRedirect(reverse('blogview', args = [pk]))