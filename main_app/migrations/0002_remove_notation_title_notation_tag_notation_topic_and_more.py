# Generated by Django 4.2.6 on 2023-11-30 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notation',
            name='title',
        ),
        migrations.AddField(
            model_name='notation',
            name='tag',
            field=models.TextField(default='default_value', max_length=100),
        ),
        migrations.AddField(
            model_name='notation',
            name='topic',
            field=models.TextField(default='default_value', max_length=100),
        ),
        migrations.AlterField(
            model_name='notation',
            name='content',
            field=models.TextField(default='default_value', max_length=100),
        ),
    ]