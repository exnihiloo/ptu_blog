from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()



class BlogPost(models.Model):
    title = models.CharField(_("title"), max_length = 255)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField(_("body"))


    def __str__(self):
        return f"{self.title} : {self.author}"