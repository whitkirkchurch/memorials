# Generated by Django 2.1.1 on 2019-03-31 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20190331_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memorial',
            old_name='names_new',
            new_name='names',
        ),
        migrations.RemoveField(
            model_name='name',
            name='memorial',
        ),
    ]