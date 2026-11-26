from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """Пользователь состоит в группе 'moderators'."""
    message = 'Доступ запрещён: требуются права модератора.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):
    """Объект принадлежит текущему пользователю."""
    message = 'Доступ запрещён: вы не владелец объекта.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
