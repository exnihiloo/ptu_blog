# Generated by Django 4.1.3 on 2022-12-07 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='images/profile.png', null=True, upload_to='user_profile/photos', verbose_name='photo'),
        ),
    ]