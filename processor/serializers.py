from rest_framework import serializers

from .models import UploadedFile


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('source_file', 'target_file')
