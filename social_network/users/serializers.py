from rest_framework import serializers
from .models import SocialUser, FriendRequest

class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ['email', 'name', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = SocialUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ['id', 'email', 'name', 'phone']
        
        
class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ['id', 'email', 'name', 'phone']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.email')
    to_user = serializers.ReadOnlyField(source='to_user.email')

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'status']