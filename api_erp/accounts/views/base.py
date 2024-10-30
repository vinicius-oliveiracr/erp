from rest_framework.views import APIView

from rest_framework.exceptions import APIException

from companies.models import Enterprise, Employee

from accounts.models import User_Groups, Group_Permissions

from accounts.models import User

class Base(APIView):
    def get_enterprise_user(self, user_id):

        if user_id is None or not User.objects.filter(id=user_id).exists():
            
            raise APIException('User does not exist!')
            
        
        enterprise = {
            "is_owner": False,
            "permissions": []
        }

        is_owner_query  = Enterprise.objects.filter(user_id=user_id)

        if is_owner_query.exists():
            enterprise["is_owner"] = True
            return enterprise
        

        employee = Employee.objects.filter(user_id=user_id).first()

        if not employee:
            raise APIException('User is not an employee!')

        groups = User_Groups.objects.filter(user_id=user_id).all()

        for g in groups:

            group = g.group

            permissions = Group_Permissions.objects.filter(group_id=group.id).all()

            for p in permissions:
                enterprise["permissions"].append({
                    "id": p.permission.id,
                    "label": p.permission.name,
                    "codename": p.permission.codename
                })

        return enterprise