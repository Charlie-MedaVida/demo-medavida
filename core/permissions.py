from django.contrib.auth.models import User
from guardian.shortcuts import get_perms
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework_api_key.permissions import BaseHasAPIKey
from core.models import UserAPIKey


def check_user_has_credits(user: User) -> Response | None:
    """
    Returns a 402 Response if the user has no credits remaining, otherwise None.

    Usage at the top of a view method:
        error = check_user_has_credits(user)
        if error:
            return error
    """
    if user.profile.credit_count <= 0:
        return Response(
            {'message': 'Insufficient credits.'},
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
    return None


class HasUserAPIKey(BaseHasAPIKey):
    model = UserAPIKey


class GuardianObjectPermissions(BasePermission):
    """
    Object-level permission class backed by django-guardian.

    Maps each HTTP method to a guardian permission codename and verifies
    that the requesting user holds that permission on the specific object.
    Requires the user to be authenticated.
    """

    perms_map = {
        'GET': 'view_{model_name}',
        'HEAD': 'view_{model_name}',
        'OPTIONS': 'view_{model_name}',
        'PUT': 'change_{model_name}',
        'PATCH': 'change_{model_name}',
        'DELETE': 'delete_{model_name}',
    }

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        model_name = obj.__class__._meta.model_name
        required_perm = self.perms_map.get(request.method, '')
        if not required_perm:
            return False
        perm = required_perm.format(model_name=model_name)
        return perm in get_perms(request.user, obj)