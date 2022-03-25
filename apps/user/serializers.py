from rest_framework import serializers

from apps.user.models import User


# simplejwt drf-yasg integration
# drf-yasg 통합을 위해 선언 되었음
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class UserListSerializer(serializers.ModelSerializer):
    user_slug = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_image = serializers.ImageField(source="user_image.source")

    def get_user_slug(self, obj):
        return obj.slug

    def get_user_name(self, obj):
        return obj.name

    class Meta:
        model = User
        fields = (
            "user_slug",
            "user_name",
            "user_image",
        )
