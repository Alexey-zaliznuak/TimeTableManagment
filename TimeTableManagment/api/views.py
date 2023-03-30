from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ClassRoomsSerializer,
    LessonTypesSerializer,
    GroupsSerializer,
    LessonsSerializer,
    ActivitiesSerializer,
    StudentsSerializer,
    TeachersSerializer,
    MethodistsSerializer
)

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

class ClassRoomsViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomsSerializer

class LessonTypesViewSet(viewsets.ModelViewSet):
    queryset = LessonType.objects.all()
    serializer_class = LessonTypesSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

class LessonsViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonsSerializer

class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer

class TeachersViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeachersSerializer

class MethodistsViewSet(viewsets.ModelViewSet):
    queryset = Methodist.objects.all()
    serializer_class = MethodistsSerializer
