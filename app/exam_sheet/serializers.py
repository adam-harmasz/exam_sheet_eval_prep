from rest_framework import serializers

from core import models


class ExamSheetSerializer(serializers.ModelSerializer):
    """Serializer for ExamSheet objects"""

    class Meta:
        model = models.ExamSheet
        fields = ('id', 'name', 'owner', 'total_points', 'grade', 'student')
        read_only_fields = ('id',)
