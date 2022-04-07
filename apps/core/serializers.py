from rest_framework.serializers import ModelSerializer

from apps.core.models import Image


class ImageSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = ("source",)
