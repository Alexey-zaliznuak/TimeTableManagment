from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, ROLE_PREFIX
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from timetables.apps import TimetablesConfig
from multiselectfield import MultiSelectField


APP_NAME = TimetablesConfig.name


DAYS = (
    ('monday', 'monday'),
    ('tuesday', 'tuesday'),
    ('wednesday', 'wednesday'),
    ('thursday', 'thursday'),
    ('friday', 'friday'),
    ('saturday', 'saturday'),
    ('sunday', 'sunday'),
)


class RoleModel(models.Model):
    can_edit_timetable = False

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        abstract = True

class EventModel(models.Model):
    day = models.SmallIntegerField("День в расписании")
    start_time = models.TimeField("Время начала")
    duration = models.TimeField("Продолжительность")

    class Meta:
        abstract = True

class Group(models.Model):
    name = models.CharField('Группа', max_length=64)

    def __str__(self) -> str:
        return self.name

class Student(RoleModel):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name=ROLE_PREFIX + 'Student',
    )
    group = models.ForeignKey(
        Group,
        related_name='students',
        verbose_name='Группа',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.user.username + ' ' + self.group.name

class Teacher(RoleModel):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name=ROLE_PREFIX + 'Teacher',
    )
    work_days = MultiSelectField(
        "Рабочие дни",
        choices=DAYS,
        blank=True,
        null=True,
    )
    # TODO командировки, отпуска

    def can_teach(lesson_dt) -> bool:
        # if lesson_dt not in methodic days
        # if lesson_dt not in hlidays
        return True

class Methodist(RoleModel):
    can_edit_timetable = True
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name=ROLE_PREFIX + 'Methodist'
    )

class ClassRoom(models.Model):
    number = models.CharField("Аудитория", max_length=128)

    def __str__(self) -> str:
        return self.number

class LessonType(models.Model):
    name = models.CharField('Наименование дисциплины', max_length=64)

    def __str__(self) -> str:
        return self.name

class Lesson(EventModel):
    class SubGroupChoices(models.IntegerChoices):
        ALL = 0, _('Вся группа')
        FIRST = 1, _('Первая')
        SECOND = 2, _('Вторая')

    groups = models.ManyToManyField(
        Group,
        related_name='lessons',
        verbose_name='Группа(ы)',
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Преподователь',
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Кабинет',
    )
    lesson_type = models.ForeignKey(
        LessonType,
        related_name='lessons',
        verbose_name='Дисциплина',
        on_delete=models.CASCADE,
    )

    day = models.SmallIntegerField("День в расписании")
    start_time = models.TimeField("Начало урока")
    duration = models.TimeField("Продолжительность урока")

    subgroup = models.SmallIntegerField(
        "Подгруппа(ы)",
        choices=SubGroupChoices.choices,
        default=SubGroupChoices.ALL,
    )

class Activity(EventModel):
    groups = models.ManyToManyField(
        Group,
        related_name='activities',
        verbose_name='Группа(ы)',
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='Преподователь(если ведет)',
        blank=True,
        null=True,
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='Кабинет (если есть)',
        blank=True,
        null=True,
    )
