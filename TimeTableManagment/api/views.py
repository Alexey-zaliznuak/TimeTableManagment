from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .permissions import (
    MethodistOrCanEditAllOrReadOnly,
    CanEditAllOrReadOnly,
    YourRoleOrReadOnly,
)

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
    permission_classes = (MethodistOrCanEditAllOrReadOnly, )

class LessonTypesViewSet(viewsets.ModelViewSet):
    queryset = LessonType.objects.all()
    serializer_class = LessonTypesSerializer
    permission_classes = (MethodistOrCanEditAllOrReadOnly, )

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = (MethodistOrCanEditAllOrReadOnly, )

class LessonsViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = (MethodistOrCanEditAllOrReadOnly, )

class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer
    permission_classes = (MethodistOrCanEditAllOrReadOnly, )

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = (YourRoleOrReadOnly, )

class TeachersViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeachersSerializer
    permission_classes = (MethodistOrCanEditAllOrReadOnly, )

class MethodistsViewSet(viewsets.ModelViewSet):
    queryset = Methodist.objects.all()
    serializer_class = MethodistsSerializer
    permission_classes = (CanEditAllOrReadOnly, )
