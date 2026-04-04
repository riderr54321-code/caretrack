from django import template

register = template.Library()

@register.filter
def user_role(user):
    """Safely get user role, returns 'doctor' as default"""
    try:
        if hasattr(user, 'userprofile') and user.userprofile:
            return user.userprofile.role
    except:
        pass
    return 'doctor'
