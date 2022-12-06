from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import datetime, date
from PIL import Image



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
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), related_name='blogpost_topics', on_delete=models.CASCADE)
    image = models.ImageField(_("image"), null = True, blank = True, upload_to='images/', default = 'images/default.png')
    users_readlater = models.ManyToManyField(User, related_name="user_readlater", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            if image.width > 300 or image.height > 300:
                output_size = (300, 300)
                image.thumbnail(output_size)
                image.save(self.image.path)


    def get_absolute_url(self):
        return reverse("blogview")


    def __str__(self):
        return f"{self.title} : {self.author}"

    def get_absolute_url(self):
        return reverse('home')
        
    
class BlogComment(models.Model):
    blogpost = models.ForeignKey(BlogPost, related_name = 'comments', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateField(_("created at"), auto_now_add = True)
    content = models.TextField(_("content"), max_length=2000)


    def __str__(self):
        return self.user.username