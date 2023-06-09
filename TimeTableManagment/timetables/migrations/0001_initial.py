# Generated by Django 3.2 on 2023-03-28 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=128, verbose_name='Аудитория')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Группа')),
            ],
        ),
        migrations.CreateModel(
            name='LessonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование дисциплины')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_days', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thursday', 'thursday'), ('friday', 'friday'), ('saturday', 'saturday'), ('sunday', 'sunday')], max_length=56, null=True, verbose_name='Рабочие дни')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roleTeacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='timetables.group', verbose_name='Группа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roleStudent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Methodist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roleMethodist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.SmallIntegerField(verbose_name='День в расписании')),
                ('start_time', models.TimeField(verbose_name='Начало урока')),
                ('duration', models.TimeField(verbose_name='Продолжительность урока')),
                ('subgroup', models.SmallIntegerField(choices=[(0, 'Вся группа'), (1, 'Первая'), (2, 'Вторая')], default=0, verbose_name='Подгруппа(ы)')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='timetables.classroom', verbose_name='Кабинет')),
                ('groups', models.ManyToManyField(related_name='lessons', to='timetables.Group', verbose_name='Группа(ы)')),
                ('lesson_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='timetables.lessontype', verbose_name='Дисциплина')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='timetables.teacher', verbose_name='Преподователь')),
            ],
        ),
    ]
