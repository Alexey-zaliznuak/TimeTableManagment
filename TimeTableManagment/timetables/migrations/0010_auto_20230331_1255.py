# Generated by Django 3.2 on 2023-03-31 09:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0009_alter_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='day',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(13)], verbose_name='День в расписании'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(default='default migration name', max_length=150, verbose_name='Наименование мероприятия'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='day',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(13)], verbose_name='День в расписании'),
        ),
    ]
