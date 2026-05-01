from functools import wraps

from rest_framework.exceptions import PermissionDenied

# def admin_required(func):
#     """
#     Decorator to ensure the user is an admin. Raises PermissionDenied if not.
#     """
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_admin:  # Check if user is admin
#             raise PermissionDenied("You do not have permission to access this resource.")
#         return func(request, *args, **kwargs)
#     return wrapper


def custom_permissions(is_admin=False, groups=None):
    """
    Check if the user is an admin and/or optionally belongs to a specific group.

    Args:
        is_admin (bool): Whether the user must be an admin. Default is False.
        group (str, optional): If provided, checks if the user belongs to this group.

    Returns:
        function: A decorator that can be applied to view methods.
    """
    def decorator(func):

        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            # Admin check
            if is_admin:
                if not getattr(user, 'is_admin', False):
                    raise PermissionDenied(
                        "You do not have permission to access this resource.")
            # Group check
            if groups:
                # convert user groups to lower case
                user_groups = [g.lower()
                               for g in getattr(user, 'user_groups', [])]
                # user must belong to atleast one of the specified groups
                if not any(g.lower() in user_groups for g in groups):
                    raise PermissionDenied(
                        f"You must belong to one of the groups {groups} to access this resource.")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
