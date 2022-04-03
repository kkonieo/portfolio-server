from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from apps.project.models import Project
from apps.project.serializers import ProjectSerializer
from apps.tag.models import Position, Tech
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
class TokenObtainPairResponseSerializer(Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenBlacklistResponseSerializer(Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class UserListSerializer(ModelSerializer):
    user_slug = SerializerMethodField()
    user_name = SerializerMethodField()
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


class LinkSerializer(ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = Link
        fields = ("id", "source")


class DevelopedFunctionSerializer(ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = DevelopedFunction
        fields = "__all__"


class EducationSerializer(ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = Education
        fields = "__all__"


class OtherExperienceSerializer(ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = OtherExperience
        fields = "__all__"


class CareerSerializer(ModelSerializer):
    # user_slug = serializers.CharField(source="user.slug", read_only=True)

    class Meta:
        model = Career
        fields = ("company", "positions", "tech")


class ListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class UserSerializer(ModelSerializer):
    user_slug = serializers.CharField(source="slug", read_only=True)
    user_name = serializers.CharField(source="name", allow_null=True)
    user_image = serializers.ImageField(
        source="user_image.source",
        allow_null=True,
        allow_empty_file=True,
        read_only=True,
    )
    user_introduction = serializers.CharField(source="introduction", allow_null=True)

    user_positions = PositionSerializer(
        source="positions", many=True, allow_null=True, required=False, read_only=True
    )
    skills = TechSerializer(
        source="tech", many=True, allow_null=True, required=False, read_only=True
    )
    projects = SerializerMethodField(allow_null=True, read_only=True)
    user_links = SerializerMethodField(allow_null=True, read_only=True)
    careers = SerializerMethodField(allow_null=True, read_only=True)
    educations = SerializerMethodField(allow_null=True, read_only=True)
    other_experiences = SerializerMethodField(allow_null=True, read_only=True)
    developed_functions = SerializerMethodField(allow_null=True, read_only=True)

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

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('user_name', instance.name)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.save()
    #     return instance

    class Meta:
        model = User
        fields = (
            "user_slug",
            "user_name",
            "user_image",
            "user_introduction",
            "hobby",
            "expected_salary",
            "user_positions",
            "skills",
            "projects",
            "user_links",
            "careers",
            "educations",
            "other_experiences",
            "developed_functions",
        )
