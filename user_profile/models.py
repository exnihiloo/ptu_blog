from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name="profile",
    )
    photo = models.ImageField(_("photo"), upload_to='user_profile/photos', null=True, blank=True)
    about = models.TextField(_("about"), max_length=2000)

    def __str__(self) -> str:
        return f"{self.user} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            photo = Image.open(self.photo.path)
            if photo.width > 500 or photo.height > 500:
                output_size = (500, 500)
                photo.thumbnail(output_size)
                photo.save(self.photo.path)