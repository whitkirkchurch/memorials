# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-07 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170323_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='memorial',
            name='complete',
            field=models.BooleanField(default=False, help_text="Should this memorial's record be considered complete?"),
            preserve_default=False,
        ),
    ]