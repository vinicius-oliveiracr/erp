from rest_framework import serializers

from django.contrib.auth.models import Permission

from accounts.models import User_Groups, User, Group, Group_Permissions

from companies.models import Employee, Task


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        name = serializers.SerializerMethodField()
        email = serializers.SerializerMethodField()

class EmployeesSerializer (serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email'
        )

    def get_name (self, obj):

        return obj.user.name
    
    def get_email (self, obj):

        return obj.user.email
    
    class EmployeeSerializer (serializers.ModelSerializer):

        name = serializers.SerializerMethodField()
        email = serializers.SerializerMethodField()
        groups = serializers.SerializerMethodField()

        class Meta:
            model = Employee
            fields = (
                'id',
                'name',
                'email',
                'groups'
            )

        def get_name (self, obj):

            return obj.user.name
        
        def get_email (self, obj):

            return obj.user.email
        
        def get_groups(self,obj):

            groupsDB = User_Groups.objects.filter(user_id=obj.user.id).all()

            groups_data = []

            for group in groupsDB:

                groups_data.append({
                    "id": group.group.id,
                    "name": group.group.name
                })

            return groups_data
        

class GroupsSerializer (serializers.ModelSerializer):

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions'
        )

    def get_permissions (self, obj):

        groups = Group_Permissions.objects.filter()

        permissions = []

        for group in groups:

            permissions.append({
                "id": group.permission.id,
                "label": group.permission.name,
                "codename": group.permission.codename
            })

        return permissions
    

class PermissionsSerializer (serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'codename'
        )


class TasksSerializer (serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'created_at',
            'status'
        )

    def get_status (self, obj):

        return obj.status.name
    

class TaskSerializer (serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    employee = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'created_at',
            'status',
            'employee'
        )


    def get_status(self, obj):

        return obj.status.name
    
    def get_employee(self, obj):

        return EmployeesSerializer(obj.employee).data