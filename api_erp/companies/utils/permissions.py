from rest_framework import permissions

from accounts.models import User_Groups, Group_Permissions

from django.contrib.auth.models import Permission

def check_permission(user, method, permission_to):
    if not user.is_authenticated:
        return False
    
    if user.is_owner:
        return True
    
    required_permission = 'view_' + permission_to

    if method == 'POST':

        required_permission = 'add_' + permission_to

    elif method == 'PATCH' or method == 'PUT':

        required_permission = 'change_' + permission_to

    elif method == 'DELETE':

        required_permission = 'delete_' + permission_to

    groups = User_Groups.objects.values('group_id').filter(user_id=user.id).all()

    for group in groups:

        permissions = Group_Permissions.objects.values('permission_id').filter(group_id=group['group_id']).all()

        for permission in permissions:

            if Permission.objects.filter(id=permission['permission_id'], codename = required_permission).exists():
                return True
            

class EmployeesPermission(permissions.BasePermission):

    message = "Employee does not have employee management permission"

    def has_permission(self, request, _view):

        return check_permission(request.user, request.method, 'employee')
    

class GroupsPermission (permissions.BasePermission):

    message = "Employee does not have group management permission"

    def has_permission(self, request, _view):

        return check_permission(request.user, request.method, 'group')
    

class GroupsPermissionsPermission (permissions.BasePermission):

    message = "Employee does not have permission management permission"

    def has_permission(self, request, _view):
        
        return check_permission(request.user, request.method, 'permission')
    

class TaskPermission (permissions.BasePermission):

    message = "Employee does not have task management permission"

    def has_permission(self, request, _view):

        return check_permission(request.user, request.method, 'task')