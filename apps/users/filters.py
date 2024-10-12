from dj_rest_kit.filters import BaseFilter, BaseOrderingFilter

from apps.users import models


class UserFilter(BaseFilter):
    class Meta:
        model = models.User
        fields = ('email', 'mobile_number', )

    ordering = (BaseOrderingFilter(
        fields=(
            ('id', 'id'),
        )))
