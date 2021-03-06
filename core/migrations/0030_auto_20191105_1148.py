# Generated by Django 2.1.8 on 2019-11-05 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20190401_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memorial',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='memorial',
            name='longitude',
        ),
        migrations.AddField(
            model_name='name',
            name='died_aged',
            field=models.IntegerField(blank=True, help_text='If known, the age of this person when they died.', null=True),
        ),
    ]
