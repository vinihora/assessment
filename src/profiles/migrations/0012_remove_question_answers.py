# Generated by Django 3.2.5 on 2021-07-13 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_category_choices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answers',
        ),
    ]
