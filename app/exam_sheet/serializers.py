from rest_framework import serializers
from rest_framework.reverse import reverse_lazy, reverse

from core import models


class AnswerSerializer (serializers.ModelSerializer):
    """Serializer for Answer objects"""
    url = serializers.SerializerMethodField('answer_url')

    class Meta:
        model = models.Answer
        fields = ('id', 'task', 'answer', 'is_correct', 'url')
        read_only_fields = ('id',)

    def answer_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('exam:answer-detail', args=[obj.id], request=request)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""
    # task_answer = serializers.SerializerMethodField('list_of_answers')
    task_answer = AnswerSerializer(many=True)
    url = serializers.SerializerMethodField('task_url')

    class Meta:
        model = models.Task
        fields = ('id',
                  'name',
                  'exam_sheet',
                  'question',
                  'task_answer',
                  'points_to_achieve',
                  'url')
        read_only_fields = ('id',)

    def list_of_answers(self, obj):
        """Nested Answer serializer"""
        serializer = AnswerSerializer(obj.task_answer.all(), many=True)
        return serializer.data

    def task_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('exam:task-detail', args=[obj.id], request=request)


class ExamSheetSerializer(serializers.ModelSerializer):
    """Serializer for ExamSheet objects"""
    # exam_task = serializers.SerializerMethodField('list_of_tasks')
    exam_task = TaskSerializer(many=True, required=False)
    url = serializers.SerializerMethodField('exam_url')

    class Meta:
        model = models.ExamSheet
        fields = ('id',
                  'name',
                  'owner',
                  'exam_task',
                  'number_of_copies',
                  'is_finished',
                  'url',
                  )
        read_only_fields = ('id',)

    def list_of_tasks(self, obj):
        """Nested Task serializer"""
        serializer = TaskSerializer(obj.exam_task.all(), many=True)
        return serializer.data

    def exam_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('exam:exam-detail', args=[obj.id], request=request)
