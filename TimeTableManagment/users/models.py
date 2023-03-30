from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


METHODIST = 'Methodist'
ROLES_APP = 'timetables'
ROLE_PREFIX = 'role'


class User(AbstractUser):
    email = models.EmailField(_('Электронная почта'), max_length=254, unique=True)

    def clean(self) -> None:
        #  username validation
        if self.username == 'me':
            raise ValidationError('uncorrect username')

    @property
    def role(self):
        for rel in self._meta.related_objects:
            if rel.related_name and rel.related_name.startswith(ROLE_PREFIX):
                value = self.__getattribute__(rel.related_name).first()
                if value:
                    return {
                        'name': rel.related_name[len(ROLE_PREFIX):],
                        'value': value
                    }

    @property
    def is_methodist(self) -> bool:
        role = self.role
        if not role:
            return False

        return self.role['name'] == METHODIST

    @property
    def can_edit_all_users(self) -> bool:
        return (
            self.is_superuser
            or self.is_staff
        )

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.username
