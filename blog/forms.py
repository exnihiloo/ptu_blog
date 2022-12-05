from django import forms
from . import models

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPost
        fields = ('title', 'title_tag', 'author', 'body')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}),
            'title_tag' : forms.TextInput(attrs={'class':'form-control'}),
            'author' : forms.Select(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Write your story here'}),
        }


class EditBlogPostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPost
        fields = ('title','title_tag', 'body',)

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}),
            'title_tag' : forms.TextInput(attrs={'class':'form-control'}),
            'body' : forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Write your story here'}),
        }