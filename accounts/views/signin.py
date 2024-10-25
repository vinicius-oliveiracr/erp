from rest_framework.views import APIView

from accounts.auth import Authentication

from accounts.serializers import UserSerializer

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny

from accounts.views.base import Base

class Signin(Base, APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    print("Signin request")

    email = request.data.get('email')
    password = request.data.get('password')

    print(f"Email: {email}  Password: {password}")

    try:
      auth = Authentication()

      user = auth.signin(request, email=email, password=password)

      token = RefreshToken.for_user(user)

      enterprise = self.get_enterprise_user(user.id)

      serializer = UserSerializer(user)

      print(f"User after authentication: {serializer.data}")

      print(request.user)

    except Exception as e:
      return Response({
        "details": str(e)
      })

    return Response({
        "user": serializer.data,
          "enterprise": enterprise,
          "refresh": str(token),
          "access": str(token.access_token)
        })
