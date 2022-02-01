# Generated by Django 4.0.1 on 2022-01-31 13:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('title', models.CharField(max_length=255, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
            ],
            options={
                'verbose_name_plural': '게시글',
                'db_table': 'post',
            },
        ),
    ]
