# Generated by Django 2.1.1 on 2019-03-23 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190323_2043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='name',
            options={'ordering': ['family_name', 'given_names']},
        ),
    ]
