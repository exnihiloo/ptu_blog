from django.contrib import admin
from . import models

admin.site.register(models.BlogPost)
admin.site.register(models.Topic)
admin.site.register(models.BlogComment)
admin.site.register(models.BlogLike)