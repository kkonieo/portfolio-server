from rest_framework import serializers

from apps.project.models import Project
from apps.project.serializers import ProjectSerializer
from apps.tag.models import Position
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


class ListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class UserSerializer(serializers.ModelSerializer):
    user_slug = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_image = serializers.ImageField(source="user_image.source", allow_null=True)
    user_positions = ListingField(
        source="positions",
        many=True,
        allow_null=True,
        read_only=True,
    )
    user_links = serializers.SerializerMethodField()
    user_introduction = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    skills = ListingField(
        source="tech",
        many=True,
        allow_null=True,
        read_only=True,
    )
    careers = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    other_experiences = serializers.SerializerMethodField()
    developed_functions = serializers.SerializerMethodField()

    def get_user_slug(self, obj):
        return obj.slug

    def get_user_name(self, obj):
        return obj.name

    def get_user_introduction(self, obj):
        return obj.introduction

    def get_user_links(self, obj):
        links = Link.objects.filter(user=obj)
        serializer = LinkSerializer(
            links,
            many=True,
            allow_null=True,
            read_only=True,
        )
        return serializer.data

    def get_projects(self, obj):
        projects = Project.objects.filter(author=obj)
        serializer = ProjectSerializer(
            projects,
            many=True,
            allow_null=True,
            read_only=True,
        )
        return serializer.data

    def get_careers(self, obj):
        careers = Career.objects.filter(user=obj)
        serializer = CareerSerializer(
            careers,
            many=True,
            allow_null=True,
            read_only=True,
        )
        return serializer.data

    def get_educations(self, obj):
        educations = Education.objects.filter(user=obj)
        serializer = EducationSerializer(
            educations,
            many=True,
            allow_null=True,
            read_only=True,
        )
        return serializer.data

    def get_other_experiences(self, obj):
        other_experiences = OtherExperience.objects.filter(user=obj)
        serializer = OtherExperienceSerializer(
            other_experiences,
            many=True,
            allow_null=True,
            read_only=True,
        )
        return serializer.data

    def get_developed_functions(self, obj):
        developed_functions = DevelopedFunction.objects.filter(user=obj)
        serializer = DevelopedFunctionSerializer(
            developed_functions,
            many=True,
            allow_null=True,
            read_only=True,
        )
        return serializer.data

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
