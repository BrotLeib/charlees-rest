# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-08 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='for_sale',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
