from rest_framework import serializers
from rest_framework.reverse import reverse_lazy, reverse

from core import models


class AnswerSerializer (serializers.ModelSerializer):
    """Serializer for Answer objects"""
    url = serializers.SerializerMethodField('answer_url')
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Answer
        fields = ('id', 'owner', 'task', 'answer', 'is_correct', 'url')
        read_only_fields = ('id',)

    def answer_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('answer-detail', args=[obj.id], request=request)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""
    # task_answer = serializers.SerializerMethodField('list_of_answers')
    task_answer = AnswerSerializer(many=True, required=False)
    url = serializers.SerializerMethodField('task_url')
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Task
        fields = ('id',
                  'owner',
                  'name',
                  'exam_sheet',
                  'question',
                  'task_answer',
                  'points_to_achieve',
                  'is_open_task',
                  'url')
        read_only_fields = ('id',)

    def task_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('task-detail', args=[obj.id], request=request)


class ExamSheetSerializer(serializers.ModelSerializer):
    """Serializer for ExamSheet objects"""
    # exam_task = serializers.SerializerMethodField('list_of_tasks')
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    exam_task = TaskSerializer(many=True, required=False)
    url = serializers.SerializerMethodField('exam_url')

    class Meta:
        model = models.ExamSheet
        fields = ('id',
                  'name',
                  'owner',
                  'number_of_copies',
                  'is_finished',
                  'url',
                  'exam_task',
                  )
        read_only_fields = ('id',)

    def exam_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('exam-detail', args=[obj.id], request=request)

    def update(self, instance, validated_data):
        """Updating instance"""
        instance.is_finished = validated_data.get('is_finished', instance.is_finished)
        instance.name = validated_data.get('name', instance.name)
        instance.total_points = validated_data.get('total_points',
                                                   instance.total_points)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.number_of_copies = validated_data.get('number_of_copies',
                                                       instance.number_of_copies)
        instance.save()
        return instance
