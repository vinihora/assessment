# Generated by Django 3.2.5 on 2021-07-08 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210708_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='avaliation',
        ),
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.AddField(
            model_name='avaliation',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='profiles.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='question',
            field=models.ManyToManyField(related_name='quest', to='profiles.Question'),
        ),
    ]
