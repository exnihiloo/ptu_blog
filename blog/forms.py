from django import forms
from . import models


choices = models.Topic.objects.all().values_list('name', 'name')

topics_list = []
for topic in choices:
    topics_list.append(topic)

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPost
        fields = ('title', 'title_tag', 'author', 'topic', 'body', 'image')

        widgets = {
            'title' : forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Title'}),
            'title_tag' : forms.TextInput(attrs = {'class':'form-control'}),
            'author' : forms.TextInput(attrs = {'class':'form-control', 'value' : '', 'id':'author', 'type':'hidden'}),
            'topic' : forms.Select(choices = topics_list, attrs={'class':'form-control'}),
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