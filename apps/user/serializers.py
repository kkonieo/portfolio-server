from rest_framework import serializers

from apps.project.serializers import ProjectSerializer
from apps.tag.serializers import PositionSerializer, TechSerializer
from apps.user.models import (
    Career,
    DevelopedFunction,
    Education,
    Link,
    OtherExperience,
    User,
)


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
    user_image = serializers.ImageField(source="user_image.source", allow_null=True)

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


class LinkSerializer(serializers.ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = Link
        fields = "__all__"


class DevelopedFunctionSerializer(serializers.ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = DevelopedFunction
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = Education
        fields = "__all__"


class OtherExperienceSerializer(serializers.ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = OtherExperience
        fields = "__all__"


class CareerSerializer(serializers.ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = Career
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user_slug = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_image = serializers.ImageField(source="user_image.source", allow_null=True)
    user_positions = PositionSerializer(many=True, allow_null=True)
    user_links = LinkSerializer(many=True, allow_null=True)
    user_introduction = serializers.SerializerMethodField()
    projects = ProjectSerializer(many=True, allow_null=True)
    skills = TechSerializer(many=True, allow_null=True)
    careers = CareerSerializer(many=True, allow_null=True)
    educations = EducationSerializer(many=True, allow_null=True)
    other_experiences = OtherExperienceSerializer(many=True, allow_null=True)
    developed_functions = DevelopedFunctionSerializer(many=True, allow_null=True)

    def get_user_slug(self, obj):
        return obj.slug

    def get_user_name(self, obj):
        return obj.name

    def get_user_positions(self, obj):
        return obj.positions

    def get_user_introduction(self, obj):
        return obj.introduction

    def get_skills(self, obj):
        return obj.tech

    class Meta:
        model = User
        fields = (
            "user_slug",
            "user_name",
            "user_image",
            "user_positions",
            "user_links",
            "user_introduction",
            "projects",
            "skills",
            "careers",
            "educations",
            "other_experiences",
            "developed_functions",
            "hobby",
            "expected_salary",
        )
