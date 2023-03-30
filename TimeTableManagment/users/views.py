from .models import User
from .permissions import UsersPermission
from .serializers import (
    UserSerializer,
)

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UsersPermission,)
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', "patch", 'delete']

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        filter_backends=(),
        serializer_class=UserSerializer,
    )

    def me(self, request):
        self.kwargs.update(username=request.user.username)
        if request.method == 'PATCH':
            return self.partial_update(request, request.user.username)

        return self.retrieve(request, request.user.username)
