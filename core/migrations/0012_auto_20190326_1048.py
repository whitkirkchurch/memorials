# Generated by Django 2.1.1 on 2019-03-26 10:48

import autoslug.fields
from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190323_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('description', markdownx.models.MarkdownxField()),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='name', unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='memorial',
            name='tags',
            field=models.ManyToManyField(to='core.Tag'),
        ),
    ]
