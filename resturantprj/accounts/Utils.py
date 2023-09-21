from django.core.exceptions import PermissionDenied

def DetectUser(user):
    if user.role == 1:
        return "VDashBoard"
    elif user.role == 2:
        return "CDashBoard"
    elif user.role is None and user.is_admin:
        return "/admin"
    
# check permission to visit Customer dashboard or vendor dash board  

def check_role_customer(user):
    if user.role == 2:
        return True
    
    else :
        raise PermissionDenied
    
def check_role_vendor(user):
    if user.role == 1:
        return True
    
    else :
        raise PermissionDenied

