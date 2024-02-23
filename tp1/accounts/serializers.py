from .models import User

from rest_framework import serializers
from . import validators


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators = validators.unique_username)
    email = serializers.CharField(validators = validators.unique_email)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {
            # ! can not specify extra kwargs for confirm password here cuz
            # ! it's not a model field
            "password": {"write_only": True}, # means only to use in post put (send)
            # "confirm_password": {"write_only": True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs["confirm_password"]:
            raise serializers.ValidationError({'confirm_password' : 'Make sure is the same as password.'})
        attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user