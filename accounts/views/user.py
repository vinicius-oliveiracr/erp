from accounts.views.base import Base

from accounts.models import User

from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserSerializer

from rest_framework.response import Response

from rest_framework.exceptions import APIException

class GetUser(Base):

    permission_classes = [IsAuthenticated]

    def get(self, request) -> None:
        try:
            print(f"Authenticated User: {request.user}")
            
            user = User.objects.filter(id=request.user.id).first()
            print(f"User id: {request.user.id}. Found user: {user}")

            if not user:
                return Response({
                    "detail": "user not fount",
                    "code":"user_not_found"
                }, status=404)

            enterprise = self.get_enterprise_user(user)

            serializer = UserSerializer(user)

            return Response({
                "user": serializer.data,
                "enterprise": enterprise
                })
        
        except Exception as e:
            return Response({
                "detail": f"An error occurred: {str(e)}",
                "code": "internal_server_error"
            }, status=500)