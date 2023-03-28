from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'profession',
            'object_id',
        ]

    def update(self, user, validated_data):
        for key, value in validated_data.items():
            if (
                key in ['proffesion', 'object_id']
                and not user.can_edit_default_content
            ):
                value = user.role

            user.__setattr__(key, value)

        user.save()
        return user
