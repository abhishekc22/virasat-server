from rest_framework import serializers 
from.models import *



class Usersignupserializer(serializers.ModelSerializer): 
    class Meta:
        model=CustomUser
        fields='__all__'

class Loginseralizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

 