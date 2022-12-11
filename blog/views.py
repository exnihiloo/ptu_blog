from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import BlogPost, Topic, BlogLike
from django.shortcuts import render, get_object_or_404
from .forms import BlogPostForm, EditBlogPostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _


class Home(ListView):
    model = BlogPost
    paginate_by = 3
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
            messages.error(self.request, _("Your comment was posted."), extra_tags='comment')
            return self.form_valid(form)
        else:
            messages.error(self.request, _("Malaka, you're posting too much!"), extra_tags='comment')
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




class CreateBlog(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'add_blogpost.html'

    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(CreateBlog, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context


class EditBlog(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = EditBlogPostForm
    template_name = 'edit_blog.html'

    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(EditBlog, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context


class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'delete_blog.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        item_menu = Topic.objects.all()
        context = super(DeleteBlog, self).get_context_data(*args, **kwargs)
        context['item_menu'] = item_menu
        return context

    

class CreateTopic(LoginRequiredMixin, CreateView):
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
    paginate = Paginator(BlogPost.objects.filter(topic = topic), 2)
    page = request.GET.get('page')
    topic_blogposts = paginate.get_page(page)
    nums = "a" * topic_blogposts.paginator.num_pages
    return render(request, 'topics.html', {'topic' : topic, 'topic_blogposts' : topic_blogposts, 'nums' : nums})



def search(request):
    query = request.GET.get('query')
    search_results = BlogPost.objects.filter(Q(title__icontains=query) | 
        Q(author__username__icontains=query) | 
        Q(topic__name__icontains=query) 
    )
    page = request.GET.get('page')
    paginator = Paginator(search_results, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    nums = "a" * posts.paginator.num_pages
    return render(request, 'search.html', {'blogposts': search_results, 'query': query, 'blogposts' : posts, 'nums' : nums})

@login_required
def likes(request, pk):
    user = request.user
    blogpost = BlogPost.objects.get(id = pk)
    current_likes = blogpost.likes
    liked = BlogLike.objects.filter(user = user, liked_blog = blogpost).count()
    if not liked:
        liked = BlogLike.objects.create(user = user, liked_blog = blogpost)
        current_likes += 1
        messages.success(request, _("You liked this blog post."))
    else:
        liked = BlogLike.objects.filter(user = user, liked_blog = blogpost).delete()
        current_likes -= 1
        messages.success(request, _("You unliked this blog post."))
    blogpost.likes = current_likes
    blogpost.save()
    return HttpResponseRedirect(reverse('blogview', args = [pk]))