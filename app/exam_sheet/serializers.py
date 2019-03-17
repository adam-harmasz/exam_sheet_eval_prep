from rest_framework import serializers

from core import models


class AnswerSerializer (serializers.ModelSerializer):
    """Serializer for Answer objects"""

    class Meta:
        model = models.Answer
        fields = ('id', 'task', 'is_correct')
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""
    task_answer = serializers.SerializerMethodField('list_of_answers')

    class Meta:
        model = models.Task
        fields = ('id',
                  'name',
                  'exam_sheet',
                  'question',
                  'user_answer',
                  'points_to_achieve')
        read_only_fields = ('id',)

    def list_of_answers(self, obj):
        """Nested Answer serializer"""
        serializer = AnswerSerializer(obj.task_answer.all(), many=True)
        return serializer.data


class ExamSheetSerializer(serializers.ModelSerializer):
    """Serializer for ExamSheet objects"""
    exam_task = serializers.SerializerMethodField('list_of_tasks')

    class Meta:
        model = models.ExamSheet
        fields = ('id',
                  'name',
                  'owner',
                  'total_points',
                  'grade',
                  'student',
                  'exam_task')
        read_only_fields = ('id',)

    def list_of_tasks(self, obj):
        """Nested Task serializer"""
        serializer = TaskSerializer(obj.exam_task.all(), many=True)
        return serializer.data




