from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _, ngettext_lazy

class GroupLessonsLimitValidator():
    message = ngettext_lazy()