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
        return reverse('answer_student-detail', args=[obj.id], request=request)


class TaskForStudentSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""
    student_task_answer = AnswerForStudentSerializer(many=True, required=False)
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
        return reverse('task_student-detail', args=[obj.id], request=request)

    def validate(self, attrs):
        """Object validation"""
        instance = self.instance
        answers_query = instance.student_task_answer.all()
        list_of_ids = [id_ for id_ in answers_query]
        student_task_answer_id = attrs.get('student_task_answer_id')
        if student_task_answer_id in list_of_ids:
            return attrs
        raise serializers.ValidationError('Invalid answer')


class OpenTaskForStudentSerializer(serializers.ModelSerializer):
    """Serializer for OpenTaskForStudents objects"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.OpenTaskForStudent
        fields = ('id',
                  'name',
                  'exam_sheet_student',
                  'question',
                  'students_answer',
                  'url')
        read_only_fields = ('id', 'name', 'exam_sheet_student', 'question',)

    def get_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('open_task-detail', args=[obj.id], request=request)


class ExamSheetForStudentSerializer(serializers.ModelSerializer):
    """Serializer for ExamSheet objects"""
    student_exam_task = TaskForStudentSerializer(many=True, required=False)
    open_exam_task = OpenTaskForStudentSerializer(many=True, required=False)
    url = serializers.SerializerMethodField('exam_url')

    class Meta:
        model = models.ExamSheetForStudent
        fields = ('id',
                  'name',
                  'student',
                  'total_points',
                  'is_finished',
                  'student_exam_task',
                  'open_exam_task',
                  'url')
        read_only_fields = ('id', 'total_points')

    def exam_url(self, obj):
        """Add self url to serializer"""
        request = self.context.get('request')
        return reverse('exam_student-detail', args=[obj.id], request=request)

    def update(self, instance, validated_data):
        """Updating ExamSheetForStudent object"""
        instance.is_finished = validated_data.get('is_finished', instance.is_finished)
        instance.name = validated_data.get('name', instance.name)
        instance.total_points = validated_data.get('total_points',
                                                    instance.total_points)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.student = validated_data.get('student', instance.student)
        instance.save()
        return instance
