from rest_framework import serializers
from .models import UserModel
from Post.models import LikeModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password',]
        #hides password
        extra_kwargs = { #exta_kwargs and not keywargs
            'password':{'write_only':True}
        }


    #password hash
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LastUserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'last_login',
        )

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = (
            'like_user', 'like_post', 'like', 'created'
        )
