# Generated by Django 3.2.5 on 2021-07-13 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20210712_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='choices',
            field=models.ManyToManyField(related_name='choices', to='profiles.Answers'),
        ),
    ]
