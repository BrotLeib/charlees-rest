# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-09 15:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_key',
            new_name='key',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='product_type',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_city',
        ),
    ]