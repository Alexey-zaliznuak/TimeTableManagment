from datetime import datetime, timedelta, date
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User, ROLE_PREFIX
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
from django.apps import apps
from timetables.apps import TimetablesConfig
from utils import datetimes_intersect


APP_NAME = TimetablesConfig.name
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
    # use for get query set for validate
    events_models = ['Activity', 'Lesson']

    day = models.SmallIntegerField(
        "День в расписании",
        validators=[
            MinValueValidator(0),  # first monday of time table
            MaxValueValidator(WORK_DAYS), # last time_table`s saturday
        ],
    )
    start_time = models.TimeField("Время начала")
    duration = models.TimeField("Продолжительность")

    # to overrides
    geoups = None
    subgroup = None

    def validate_day(self):
        if self.day and not self.day % 7:
            raise ValidationError('It is sunday!')

    def validate_groups(self, queryset, lesson_datetime, subgroup:int = 0):
        if subgroup and self.groups.count() > 1:
            raise ValidationError(
                'Uncrorrect value: you can select one group and subgroup '
                'or select multiple groups without subgroups.'
            )

        return
        for group in self.groups.all():
            group.can_study(self.date_time, lesson_datetime, subgroup)

    def validate_teacher(self, queryset, dt):
        # check that teacher can teach
        self.teacher.can_teach(queryset, dt)

    def validate_classroom(self, queryset, dt):
        # check that room is free on date of event
        self.classroom.is_free(queryset, dt)

    def get_events_queryset(self) -> list:
        queryset = []

        for model in self.events_models:
            model = apps.get_model(APP_NAME, model)
            queryset += model.objects.all()
            # TODO add filter when create school model

        return queryset

    @property
    def date_time(self) -> tuple[datetime, datetime]:
        now = datetime.now()
        year = now.year

        if now.month < 9:
            year -= 1

        first_september = datetime(year=year, month=9, day=1)
        first_tt_week = first_september - timedelta(days=first_september.weekday())
        tt_day = (now-first_tt_week).days % (WORK_DAYS + 1)


        start_dt = now - timedelta(days = tt_day + 1) #  first monday of timetable
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

    def can_study(self, queryset, lesson_datetime:datetime, subgroup):
        "Raise validation error if group can`t study."
        pass
        # if lesson_datetime[0].strftime("%A").lower() not in self.work_days:
        #     raise ValidationError(
        #         'Teacher can`t work in this day'
        #     )

        # all_datetimes = [event.date_time for event in queryset]
        # if datetimes_intersect(
        #     lesson_datetime, all_datetimes, max_intrsects_count=2,
        # ):
        #     raise ValidationError('Teacher is already busy at this time.')

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

    vacation_start = models.DateField(
        "Дата начала отпуска", blank=True, null=True,
    )
    vacation_end = models.DateField(
        "Дата окончания отпуска", blank=True, null=True,
    )

    business_trip_start = models.DateField(
        'Дата начала командировки', blank=True, null=True,
    )
    business_trip_end = models.DateField(
        'Дата окончания командировки', blank=True, null=True,
    )

    def can_teach(self, queryset, lesson_datetime:datetime):
        """Raise validation error if can`t teach."""
        if lesson_datetime[0].strftime("%A").lower() not in self.work_days:
            raise ValidationError(
                'Teacher can`t work in this day'
            )

        new_queryset = []
        for event in queryset:
            if event.teacher == self:
                new_queryset.append(event.date_time)
        
        new_queryset += self.extra_busy_dates

        print(new_queryset)
        if datetimes_intersect(
            lesson_datetime, new_queryset, max_intrsects_count=2,
        ):
            raise ValidationError('Teacher is already busy at this time.')

    def clean(self) -> None:
        if bool(self.business_trip_start) != bool(self.business_trip_end):
            raise ValidationError(
                'Both trip`s of start and end must be selected'
            )

        if bool(self.vacation_start) != bool(self.vacation_end):
            raise ValidationError(
                'Both vocation`s of start and end must be selected'
            )

        if self.business_trip_start:
            if self.business_trip_start >= self.business_trip_end:
                raise ValidationError(
                    'Start of trip must be before end of trip date'
                )

        if self.vacation_start:
            if self.vacation_start >= self.vacation_end:
                raise ValidationError(
                    'Start of vocation must be before end of vocation date'
                )

    @property
    def extra_busy_dates(self) -> list[tuple[datetime, datetime]]:
        dates = []
        result = []

        dates.append((self.vacation_start, self.vacation_end))
        dates.append((self.business_trip_start, self.business_trip_end))

        for d in dates:

            result.append((
                datetime(d[0].year, d[0].month, d[0].day),
                datetime(d[1].year, d[1].month, d[1].day)  
            ))

        return result

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

    def is_free(self, queryset, lesson_datetime:datetime):
        "Raise validation error if classroom not is free"
        new_queryset = []
        for event in queryset:
            if event.classroom == self:
                new_queryset.append(event.date_time)

        print(new_queryset)
        if datetimes_intersect(
            lesson_datetime, new_queryset, max_intrsects_count=2,
        ):
            raise ValidationError('Room is not free at this time.')

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

    def clean(self):
        queryset = self.get_events_queryset()
        dt = self.date_time

        self.validate_day()
        self.validate_groups(queryset, dt, self.subgroup)
        self.validate_classroom(queryset, dt)
        self.validate_teacher(queryset, dt)

class Activity(EventModel):
    name = models.CharField(
        "Наименование мероприятия",
        max_length=150,
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

    def clean(self):
        queryset = self.get_events_queryset()
        dt = self.date_time

        self.validate_day()
        self.validate_groups(queryset, dt)

        if self.teacher:
            self.validate_teacher(queryset, dt)

        if self.classroom:
            self.validate_classroom(queryset, dt)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Activities'
