# Generated by Django 2.2.15 on 2020-08-26 09:21

import build_migration.todo.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20200826_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file_object',
            field=models.FileField(max_length=255, upload_to=build_migration.todo.models.get_attachment_upload_dir),
        ),
    ]
