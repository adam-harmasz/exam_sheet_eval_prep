from rest_framework import serializers
from rest_framework.reverse import reverse_lazy, reverse

from core import models


class AnswerForStudentSerializer(serializers.ModelSerializer):
    """Serializer for Answer objects"""
    # url = serializers.SerializerMethodField('answer_url')

    class Meta:
        model = models.AnswerForStudent
        fields = ('id', 'task', 'answer', 'is_correct')
        read_only_fields = ('id',)


class TaskForStudentSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""
    # task_answer = serializers.SerializerMethodField('list_of_answers')
    # task_answer = AnswerSerializer(many=True)
    # url = serializers.SerializerMethodField('task_url')

    class Meta:
        model = models.TaskForStudent
        fields = ('id',
                  'name',
                  'exam_sheet',
                  'question',
                  'students_answer',
                  'points_to_achieve')
        read_only_fields = ('id',)


class ExamSheetForStudentSerializer(serializers.ModelSerializer):
    """Serializer for ExamSheet objects"""
    # exam_task = serializers.SerializerMethodField('list_of_tasks')
    # exam_task = TaskSerializer(many=True)
    # url = serializers.SerializerMethodField('exam_url')

    class Meta:
        model = models.ExamSheetForStudent
        fields = ('id',
                  'name',
                  'owner',
                  'student',
                  'total_points',
                  'grade',
                  'is_finished'
                  )
        read_only_fields = ('id',)
