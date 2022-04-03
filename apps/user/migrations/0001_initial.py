# Generated by Django 4.0.1 on 2022-01-27 11:59

import apps.core.utility
import apps.user.models
import apps.user.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('email', models.EmailField(error_messages={'unique': '이미 사용중인 이메일 입니다.'}, max_length=60, primary_key=True, serialize=False, unique=True, verbose_name='이메일')),
                ('name', models.CharField(max_length=10, validators=[apps.user.validators.NameValidator()], verbose_name='이름')),
                ('slug', models.CharField(default=apps.core.utility.generate_random_string, max_length=20, unique=True, verbose_name='프로필 Slug')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('introduction', models.TextField(blank=True, null=True, verbose_name='자기소개')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('positions', models.ManyToManyField(blank=True, related_name='users', to='tag.Position', verbose_name='포지션')),
                ('tech', models.ManyToManyField(blank=True, related_name='users', to='tag.Tech', verbose_name='기술 목록')),
                ('user_image', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.image', verbose_name='사용자 이미지')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': '사용자',
                'db_table': 'user',
            },
            managers=[
                ('objects', apps.user.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('source', models.URLField(max_length=120, verbose_name='링크 URL')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_user', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name_plural': '링크',
                'db_table': 'link',
            },
        ),
    ]