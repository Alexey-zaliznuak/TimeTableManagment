from django.contrib import admin
from django.urls import reverse
from .models import User, ROLES_APP
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group


admin.site.unregister(Group)

@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role_object')
    empty_value_display = '-отсутствует-'


    def role_object(self, user):
        obj = user.role
        if not obj:
            return
        obj = obj.get('value')
        obj_name = obj._meta.object_name.lower()

        url = reverse(
            f'admin:{obj._meta.app_label}'
            f'_{obj_name}_change',
            kwargs={'object_id':obj.pk}
        )
        return mark_safe(
            f'<a target="_blank" href={url}>{obj_name}</a>'
        )
