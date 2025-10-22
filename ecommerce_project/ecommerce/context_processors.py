"""
Context processors to make variables available in all templates.
"""

def user_role(request):
    """
    Add user role information to all template contexts.
    """
    is_vendor = False
    if request.user.is_authenticated:
        is_vendor = request.user.groups.filter(name='Vendor').exists()
    
    return {
        'is_vendor': is_vendor,
    }
