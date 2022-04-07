# Generated by Django 4.0.1 on 2022-04-06 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('project', '0007_alter_project_ended_at_alter_project_started_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, related_name='project_image', to='core.Image', verbose_name='프로젝트 썸네일'),
        ),
    ]