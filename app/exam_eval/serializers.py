from rest_framework import serializers
from rest_framework.reverse import reverse

from core import models


class ExamSheetEvalSerializer(serializers.ModelSerializer):
    """Serializer for ExamEvaluation objects"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.ExamSheetEvaluation
        fields = ('id',
                  'student',
                  'points_to_get',
                  'points_earned',
                  'grade',
                  'comment',
                  'is_finished',
                  'url')
        read_only_fields = ('id',)

    def get_url(self, obj):
        """Create self url for serialized object"""
        request = self.context.get('request')
        return reverse('exam_eval-detail', args=[obj.id], request=request)


class StudentGradeSerializer(serializers.ModelSerializer):
    """Serializer for StudentGrade objects"""

    class Meta:
        model = models.StudentGrade
        fields = ('id', 'student', 'grade', 'exam')
        read_only_fields = ('id',)


class TaskToEvaluate(serializers.ModelSerializer):
    """Serializer for TaskToEvaluate objects"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.TaskToEvaluate
        fields = ('id',
                  'name',
                  'question',
                  'students_answer',
                  'url')
        read_only_fields = ('id',)

    def get_url(self, obj):
        """Create self url for serialized object"""
        request = self.context.get('request')
        return reverse('task_eval-detail', args=[obj.id], request=request)
