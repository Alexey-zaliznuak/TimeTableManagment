from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import (
    Lesson,  
    Student,
    Teacher,
    Methodist,
    Group,
    LessonType,
    ClassRoom,
)

def object_url(obj):
    url = reverse(
        f'admin:{obj._meta.app_label}'
        f'_{obj._meta.object_name.lower()}_change',
        kwargs={'object_id':obj.pk}
    )
    return mark_safe(
        f'<a target="_blank" href={url}>{obj}</a>'
    )


class UserRelatedAdmin(admin.ModelAdmin):
    def full_name(self, person):
        return str(person.user)

    def user_full_name(self, person):
        return object_url(person.user)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Student)
class StudentAdmin(UserRelatedAdmin):
    list_display = (
        'full_name',
        'group_name',
        'user_full_name',
    )

    def group_name(self, student):
        group = student.group

        url = reverse(
            f'admin:{group._meta.app_label}'
            f'_{group._meta.object_name.lower()}_change',
            kwargs={'object_id':group.pk}
        )
        return mark_safe(
            f'<a target="_blank" href={url}>{group.name}</a>'
        )


@admin.register(Teacher)
class TeacherAdmin(UserRelatedAdmin):
    list_display = (
        'full_name',
        'work_days',
        'user_full_name',
)


@admin.register(Methodist)
class MethodistAdmin(UserRelatedAdmin):
    list_display = (
        'full_name',
        'user_full_name',
)


@admin.register(ClassRoom)
class ClassRoomAdmin(UserRelatedAdmin):
    list_display = (
        'number',
)


@admin.register(LessonType)
class LessonTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'lesson',
        'lesson_type',
        'groups_list',
        'teacher_link',
        'classroom_link',
        'start_time',
        'duration',
        'subgroup',
    )
    search_fields = (
        'teacher',
        'classroom',
        'lesson_type',
        'start_time',
        'duration'
    )
    list_filter = ('start_time','classroom',)
    empty_value_display = '-отсутствует-'

    # костыль, убрать когда буду делать отедльно лабы лекйии и т.п
    # просто чтобы было поле как раз для ссылки на сам урок
    def lesson(self, obj):
        return "Занятие"

    def teacher_link(self, obj):
        return object_url(obj.teacher)

    def classroom_link(self, obj):
        return object_url(obj.classroom)

    def groups_list(self, obj):
        return mark_safe("\n".join([object_url(g) for g in obj.groups.all()]))
