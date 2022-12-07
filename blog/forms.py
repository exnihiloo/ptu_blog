from django import forms
from . import models
from django.utils.timezone import datetime, timedelta
from django.contrib import messages
from django.utils.translation import gettext_lazy as _



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPost
        fields = ('title', 'title_tag', 'author', 'topic', 'body', 'image')

        widgets = {
            'title' : forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Title'}),
            'title_tag' : forms.TextInput(attrs = {'class':'form-control'}),
            'author' : forms.TextInput(attrs = {'class':'form-control', 'value' : '', 'id':'author', 'type':'hidden'}),
            'topic' : forms.Select(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs = {'class':'form-control', 'placeholder': 'Write your story here'}),
            'image' : forms.FileInput(attrs = {'class': 'form-control'})
        }


class EditBlogPostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPost
        fields = ('title','title_tag', 'body', 'image')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}),
            'title_tag' : forms.TextInput(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Write your story here'}),
        }

# comments
# class CommentForm(forms.ModelForm):
#     content = forms.CharField(widget = forms.Textarea(attrs = {
#         'class': 'md-textarea form-control',
#         'rows':'4'
#     }))
#     class Meta:
#         models = models.BlogComment
#         fields = ('content', )
        

class CommentForm(forms.ModelForm):
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if valid:
            user = self.cleaned_data.get("user")
            recent_posts = models.BlogComment.objects.filter(
                user=user,
                created_at__gte=(datetime.utcnow()-timedelta(hours=1))
            ) 
            if recent_posts:
                return False
        return valid

    class Meta:
        model = models.BlogComment
        fields = ('content', 'blogpost', 'user', )
        widgets = {
            'content' : forms.Textarea(attrs = {'class':'form-control', 'placeholder': 'Comment the blog post'}),
            'blogpost': forms.TextInput(attrs = {'class':'form-control', 'value' : '', 'id':'blogpost', 'type':'hidden'}),
            'user': forms.TextInput(attrs = {'class':'form-control', 'value' : '', 'id':'user', 'type':'hidden'}),
        }
