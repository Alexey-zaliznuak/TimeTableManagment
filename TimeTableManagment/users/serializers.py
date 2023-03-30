from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'role',
        ]
        read_only_fields = ('role',)
        write_only_fields = ['password']

    def get_role(self, user):
        role = user.role

        if role:
            role['value'] = role['value'].pk
            return role

        return 'отсутствует'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
                continue

            setattr(instance, attr, value)

        instance.save()
        return instance
