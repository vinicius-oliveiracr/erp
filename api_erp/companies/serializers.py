from rest_framework import serializers

from accounts.models import User_Groups, User, Group, Group_Permissions

from django.contrib.auth.models import Permission

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        name = serializers.SerializerMethodField()
        email = serializers.SerializerMethodField()