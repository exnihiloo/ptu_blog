from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import datetime, date



User = get_user_model()


class Topic(models.Model):
    name = models.CharField(_("title"), max_length = 255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')



class BlogPost(models.Model):
    title = models.CharField(_("title"), max_length = 255)
    title_tag = models.CharField(_("title tag"), max_length = 255, default='Fox blog')
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = RichTextField(_("body"), blank = True, null = True)
    creation_date = models.DateField(_("created"), auto_now_add=True)
    topic = models.CharField(_("topic"), max_length = 255, default='sport')
    image = models.ImageField(_("image"), null = True, blank = True, upload_to='images/')


    def __str__(self):
        return f"{self.title} : {self.author}"

    def get_absolute_url(self):
        return reverse('home')
        
    