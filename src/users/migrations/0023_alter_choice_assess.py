# Generated by Django 3.2.5 on 2021-07-13 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_remove_question_answers'),
        ('users', '0022_choice_assess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='assess',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment', to='profiles.avaliation'),
        ),
    ]