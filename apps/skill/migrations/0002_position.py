# Generated by Django 4.0.1 on 2022-01-26 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='포지션')),
            ],
            options={
                'verbose_name_plural': '포지션',
                'db_table': 'position',
            },
        ),
    ]
