from rest_framework import serializers
from timetables.models import (
    ClassRoom,
    LessonType,
    Group,
    Lesson,
    Activity,
    Student,
    Teacher,
    Methodist,
)


class ClassRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class LessonTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = '__all__'


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class MethodistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Methodist
        fields = '__all__'
