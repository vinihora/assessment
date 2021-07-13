# Generated by Django 3.2.5 on 2021-07-10 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20210708_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answers',
        ),
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(related_name='answers', to='profiles.Answers'),
        ),
    ]