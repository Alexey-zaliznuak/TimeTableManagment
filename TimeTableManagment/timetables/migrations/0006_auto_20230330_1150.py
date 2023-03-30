# Generated by Django 3.2 on 2023-03-30 08:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0005_alter_activity_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='day',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='День в расписании'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='day',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='День в расписании'),
        ),
    ]