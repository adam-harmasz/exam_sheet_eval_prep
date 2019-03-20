from rest_framework import serializers
from rest_framework.reverse import reverse

from core import models


class StudentGradeSerializer(serializers.ModelSerializer):
    """Serializer for StudentGrade objects"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.StudentGrade
        fields = ('id', 'student', 'grade', 'exam', 'url')
        read_only_fields = ('id',)

    def get_url(self, obj):
        """Create self url for serialized object"""
        request = self.context.get('request')
        return reverse('student_grade-detail', args=[obj.id], request=request)

    def validate_grade(self, attrs):
        """Validate grade"""
        if 0 < attrs < 8:
            return attrs
        raise serializers.ValidationError('Grade value has to be in range 1-7')


class TaskToEvaluateSerializer(serializers.ModelSerializer):
    """Serializer for TaskToEvaluate objects"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.TaskToEvaluate
        fields = ('id',
                  'name',
                  'question',
                  'students_answer',
                  'points_to_achieve',
                  'points_earned',
                  'url')
        read_only_fields = ('id', 'name')

    def get_url(self, obj):
        """Create self url for serialized object"""
        request = self.context.get('request')
        return reverse('task_eval-detail', args=[obj.id], request=request)

    def update(self, instance, validated_data):
        """Updating instance"""
        instance.exam = validated_data.get('exam', instance.exam)
        instance.name = validated_data.get('name', instance.name)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.question = validated_data.get('question', instance.question)
        instance.students_answer = validated_data.get(
            'students_answer', instance.students_answer)
        instance.points_earned = validated_data.get(
            'points_earned', instance.points_earned)
        instance.save()
        # update ExamSheetEvaluation points
        instance.exam.points_earned += instance.points_earned
        instance.exam.save()
        return instance

    def validate(self, attrs):
        """Validate points earned"""
        points_earned = attrs.get('points_earned')
        points_to_achieve = attrs.get('points_to_achieve')
        if points_earned > points_to_achieve:
            raise serializers.ValidationError(
                'Field points earned cannot be bigger than points to achieve')
        return attrs


class ExamSheetEvalSerializer(serializers.ModelSerializer):
    """Serializer for ExamEvaluation objects"""
    exam_task_eval = TaskToEvaluateSerializer(many=True, required=False)
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
                  'url',
                  'exam_task_eval')
        read_only_fields = ('id',)

    def get_url(self, obj):
        """Create self url for serialized object"""
        request = self.context.get('request')
        return reverse('exam_eval-detail', args=[obj.id], request=request)

    def validate(self, attrs):
        """Validate points earned"""
        points_earned = attrs.get('points_earned')
        points_to_get = attrs.get('points_to_get')
        if points_earned > points_to_get:
            raise serializers.ValidationError(
                'Field points earned cannot be bigger than points to get')
        return attrs
