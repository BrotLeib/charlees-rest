# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-11 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20171011_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(default='/profiles\\profile_pictures\\default_profile_picture.jpg', upload_to='profiles/profile_pictures'),
        ),
    ]