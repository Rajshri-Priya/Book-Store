from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'location', 'mob_number', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
    
class LoginSerializer(serializers.Serializer):
    """validation by manually"""

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        # is_active is property
        if not user:
            raise serializers.ValidationError("Incorrect Credentials")
        # validated_data.update({'user': user})
        self.context.update({'user': user})
        return user