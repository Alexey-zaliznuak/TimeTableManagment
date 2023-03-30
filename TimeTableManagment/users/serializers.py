from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        ]
        read_only_fields = ('role',)

    def get_role(self, user):
        role = user.role

        if role:
            role['value'] = role['value'].pk
            return role

        return 'отсутствует'
