from rest_framework import serializers

from apps.tag.models import Position, Tech


class TechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tech
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"
