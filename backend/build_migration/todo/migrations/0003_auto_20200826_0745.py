# Generated by Django 2.2.15 on 2020-08-26 07:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0002_file'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attachment',
            new_name='File',
        ),
    ]
