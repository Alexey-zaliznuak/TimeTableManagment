from datetime import datetime, timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, ROLE_PREFIX
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError


WORK_WEEKS = 2  # 2 weeks - last sunday
WORK_DAYS = WORK_WEEKS * 7 - 1

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

    def clean(self) -> None:
        user_role = self.user.role
        self_class_name = self.__class__.__name__.lower()

        # if already has other role
        if user_role and user_role.get('name').lower() != self_class_name:
            raise ValidationError('This user already has role')

        return super().clean()

    class Meta:
        abstract = True

class EventModel(models.Model):
    day = models.SmallIntegerField(
        "День в расписании",
        validators=[
            MinValueValidator(0),  # first monday of time table
            MaxValueValidator(WORK_DAYS), # last time_table`s saturday
        ],
    )
    start_time = models.TimeField("Время начала")
    duration = models.TimeField("Продолжительность")

    def clean(self):
        self.validate_day()
        self.validate_classrooms()
        self.validate_teachers()
        self.validate_groups()

    def validate_day(self):
        if not self.day % 6:
            raise ValidationError('It is sunday!')

    def validate_groups(self):
        # groups validation
        for group in self.groups:
            can_study, msg = group.can_study(self.date_time, self.subgroup)
            if not can_study:
                raise ValidationError(
                    f'the group will not be able to show up - {msg}'
                )

    def validate_teachers(self):
        # check that teacher can teach
        can_teach, msg = self.teacher.can_teach(self.date_time)
        if not can_teach:
            raise ValidationError(
                'The teacher cannot conduct the lesson '
                f'- {msg}'
            )

    def validate_classrooms(self):
        # check that room is free on date of event
        room_is_free, msg = self.classroom.is_free(self.date_time)
        if not room_is_free:
            raise ValidationError(f'classroom is not free - {msg}')

    @property
    def date_time(self) -> tuple[datetime, datetime]:
        now = datetime.now()
        year = now.year

        if now.month < 9:
            year -= 1

        first_september = datetime(year=year, month=9, day=1)
        start_dt = (now-first_september).days % WORK_DAYS + now.weekday() + 1
        start_dt = now - timedelta(days = start_dt) #  first monday of timetable

        start_dt += timedelta(
            days=self.day,
            hours=self.start_time.hour,
            minutes=self.start_time.minute,
        )
        end_dt = start_dt + timedelta(
            hours=self.duration.hour,
            minutes=self.duration.minute,
        )

        return start_dt, end_dt

    class Meta:
        abstract = True

class Group(models.Model):
    name = models.CharField('Наименование группы', max_length=64, unique=True)

    def can_study(self, dt:datetime, subgroup) -> tuple[bool, str]:
        # TODO
        can_study = True
        msg = 'OK'
        return can_study, msg

    def __str__(self) -> str:
        return self.name

class Student(RoleModel):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name=ROLE_PREFIX + 'Student',
        unique=True,
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
        unique=True,
    )
    work_days = MultiSelectField(
        "Рабочие дни",
        choices=DAYS,
        blank=True,
        null=True,
    )
    # TODO командировки, отпуска

    def can_teach(self, lesson_datetime:datetime) -> tuple[bool, str]:
        # TODO
        msg = 'OK'
        can_teach = True
        # if lesson_dt not in methodic days
        # if lesson_dt not in hlidays
        return can_teach, msg

class Methodist(RoleModel):
    can_edit_timetable = True
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name=ROLE_PREFIX + 'Methodist',
        unique=True,
    )

class ClassRoom(models.Model):
    number = models.CharField("Аудитория", max_length=128, unique=True)

    def is_free(self, dt:datetime) -> tuple[bool, str]:
        #TODO
        is_free = True
        msg = 'OK'
        return is_free, msg

    def __str__(self) -> str:
        return self.number

class LessonType(models.Model):
    name = models.CharField(
        'Наименование дисциплины',
        max_length=64,
        unique=True
    )

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

    subgroup = models.SmallIntegerField(
        "Подгруппа(ы)",
        choices=SubGroupChoices.choices,
        default=SubGroupChoices.ALL,
    )

class Activity(EventModel):
    name = models.CharField(
        "Наименование мероприятия",
        max_length=150,
        null=True,
        blank=True,
    )
    describe = models.TextField(
        "Описание мероприятия",
        max_length=500,
        null=True,
        blank=True,
    )
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

    class Meta:
        verbose_name_plural = 'Activities'
