from rest_framework import serializers
from rest_framework.reverse import reverse_lazy, reverse

from core import models


class AnswerForStudentSerializer(serializers.ModelSerializer):
    """Serializer for Answer objects"""
    url = serializers.SerializerMethodField('answer_url')

    class Meta:
        model = models.AnswerForStudent
        fields = ('id', 'task', 'answer', 'url')
        read_only_fields = ('id', 'task', 'answer')

    def answer_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('student:answer_student-detail', args=[obj.id], request=request)


class TaskForStudentSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""
    student_task_answer = AnswerForStudentSerializer(many=True, read_only=True)
    student_task_answer_id = serializers.IntegerField(write_only=True)
    url = serializers.SerializerMethodField('task_url')

    class Meta:
        model = models.TaskForStudent
        fields = ('id',
                  'name',
                  'exam_sheet_student',
                  'question',
                  'students_answer',
                  'student_task_answer',
                  'student_task_answer_id',
                  'url')
        read_only_fields = ('id',
                            'name',
                            'exam_sheet_student',
                            'question',
                            'students_answer')

    def update(self, instance, validated_data):
        student_task_answer_id = validated_data.get('student_task_answer_id')
        instance.students_answer = student_task_answer_id
        instance.save()
        return instance

    def task_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('student:task_student-detail', args=[obj.id], request=request)


class ExamSheetForStudentSerializer(serializers.ModelSerializer):
    """Serializer for ExamSheet objects"""
    student_exam_task = TaskForStudentSerializer(many=True)
    url = serializers.SerializerMethodField('exam_url')

    class Meta:
        model = models.ExamSheetForStudent
        fields = ('id',
                  'name',
                  'student',
                  'total_points',
                  'is_finished',
                  'student_exam_task',
                  'url'
                  )
        read_only_fields = ('id', 'total_points')

    def exam_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('student:exam_student-detail', args=[obj.id], request=request)
