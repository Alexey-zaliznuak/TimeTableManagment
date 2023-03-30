from django.urls import path, include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter as Router
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import UserViewSet

from api.views import (
    ClassRoomsViewSet,
    LessonTypesViewSet,
    GroupViewSet,
    LessonsViewSet,
    ActivitiesViewSet,
    StudentViewSet,
    TeachersViewSet,
    MethodistsViewSet,
)


v1_router = Router()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('classrooms', ClassRoomsViewSet, basename='classrooms')
v1_router.register('lessontypes', LessonTypesViewSet, basename='lessontypes')
v1_router.register('groups', GroupViewSet, basename='groups')
v1_router.register('lessons', LessonsViewSet, basename='lessons')
v1_router.register('activities', ActivitiesViewSet, basename='activities')
v1_router.register('students', StudentViewSet, basename='students')
v1_router.register('teachers', TeachersViewSet, basename='teachers')
v1_router.register('methodists', MethodistsViewSet, basename='methodists')


# v1_router.register(
#     'documents_package',
#     DocumentsPackageViewSet,
#     basename='documents_package',
# )

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="TTM API",
      default_version='v1',
      description="Документация для редактора расписаний - TTM",
      contact=openapi.Contact(email="zaliznuak20@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),

   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
]
