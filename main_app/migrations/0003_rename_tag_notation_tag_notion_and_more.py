# Generated by Django 4.2.6 on 2023-11-30 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_notation_title_notation_tag_notation_topic_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notation',
            old_name='tag',
            new_name='tag_notion',
        ),
        migrations.RenameField(
            model_name='notation',
            old_name='topic',
            new_name='topic_notion',
        ),
    ]
