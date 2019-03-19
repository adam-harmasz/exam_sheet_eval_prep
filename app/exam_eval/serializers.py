from rest_framework import serializers
from rest_framework.reverse import reverse_lazy, reverse

from core import models


class ExamSheetEvalSerializer(serializers.ModelSerializer):
    """Serializer for ExamEvaluation objects"""

    class Meta:
        model = models.ExamSheetEvaluation
        fields = ('id', 'student', 'points_to_get', 'points_earned', 'grade', 'comment')
        read_only_fields = ('id',)
