# Generated by Django 3.2 on 2023-03-28 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0002_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='duration',
            field=models.TimeField(verbose_name='Продолжительность'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='start_time',
            field=models.TimeField(verbose_name='Время начала'),
        ),
    ]