# Generated by Django 4.0.1 on 2022-04-01 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
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
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to=settings.AUTH_USER_MODEL, verbose_name='이메일')),
                ('liker', models.ManyToManyField(blank=True, related_name='post_liker', to=settings.AUTH_USER_MODEL, verbose_name='좋아요누른사람')),
                ('thumbnail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.image', verbose_name='썸네일이미지')),
            ],
            options={
                'verbose_name_plural': '게시글',
                'db_table': 'post',
            },
        ),
    ]
