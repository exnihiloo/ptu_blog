from django import forms
from . import models


# choices = models.Topic.objects.all().values_list('name', 'name')

# topics_list = []
# for topic in choices:
#     topics_list.append(topic) ; choices = topics_list,

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
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget = forms.Textarea(attrs = {
        'class': 'md-textarea form-control',
        'rows':'4'
    }))
    class Meta:
        models = models.BlogComment
        fields = ('content', )