from django.contrib.auth.backends import ModelBackend

from accounts.models import User

from rest_framework.response import Response

class EmailBackend(ModelBackend):
    def authenticate(self,request, username = None, password = None, **kwargs):

        try:    
            user = User.objects.get(email=username)

        except User.DoesNotExist:
            return Response({
                "details": "User does not exist!"
            })

        if user.check_password(password):
            return user
        

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    