# Generated by Django 3.2.5 on 2021-07-12 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_choice_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='teams',
        ),
        migrations.AddField(
            model_name='teams',
            name='user',
            field=models.ManyToManyField(blank=True, to='users.Profile'),
        ),
    ]
