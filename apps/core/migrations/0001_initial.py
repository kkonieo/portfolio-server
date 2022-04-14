# Generated by Django 4.0.4 on 2022-04-14 05:44

import apps.core.utility
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('source', models.ImageField(upload_to=apps.core.utility.get_uuid_path, verbose_name='이미지')),
            ],
            options={
                'verbose_name_plural': '이미지',
                'db_table': 'image',
            },
        ),
    ]
