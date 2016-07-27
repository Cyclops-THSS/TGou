# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGouApp', '0009_auto_20160728_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='message',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
