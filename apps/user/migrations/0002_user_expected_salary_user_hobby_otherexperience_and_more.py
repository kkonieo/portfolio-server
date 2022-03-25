# Generated by Django 4.0.1 on 2022-03-24 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expected_salary',
            field=models.IntegerField(blank=True, null=True, verbose_name='희망 연봉'),
        ),
        migrations.AddField(
            model_name='user',
            name='hobby',
            field=models.TextField(blank=True, null=True, verbose_name='취미'),
        ),
        migrations.CreateModel(
            name='OtherExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='시작일')),
                ('ended_at', models.DateTimeField(blank=True, null=True, verbose_name='종료일')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='경험명')),
                ('achievement', models.TextField(blank=True, null=True, verbose_name='이수 교과 또는 주요 성취 등')),
                ('tech', models.ManyToManyField(blank=True, null=True, related_name='other_experiences', to='tag.Tech', verbose_name='경험에서 사용한 기술 목록')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_experience_user', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Functions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='기능명')),
                ('description', models.TextField(blank=True, null=True, verbose_name='기능 설명')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_user', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='시작일')),
                ('ended_at', models.DateTimeField(blank=True, null=True, verbose_name='종료일')),
                ('school', models.CharField(blank=True, max_length=50, null=True, verbose_name='학교명')),
                ('status', models.CharField(default='졸업', max_length=10, verbose_name='재학 또는 졸업 상태')),
                ('department', models.CharField(default='컴퓨터공학과', max_length=50, verbose_name='학과')),
                ('gpa', models.FloatField(default=3.5, verbose_name='학점')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education_user', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='시작일')),
                ('ended_at', models.DateTimeField(blank=True, null=True, verbose_name='종료일')),
                ('company', models.CharField(blank=True, max_length=50, null=True, verbose_name='회사명')),
                ('positions', models.ManyToManyField(blank=True, related_name='careers', to='tag.Position', verbose_name='포지션')),
                ('tech', models.ManyToManyField(blank=True, related_name='careers', to='tag.Tech', verbose_name='기술 목록')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='career_user', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]