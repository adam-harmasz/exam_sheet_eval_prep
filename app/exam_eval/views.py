from rest_framework import viewsets, mixins
from django_filters import rest_framework as filters

from exam_sheet.permissions import IsOwner, IsTeacher
from . import serializers
from core import models


class ExamSheetEvalViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheetEvaluation serialized data"""
    queryset = models.ExamSheetEvaluation.objects.all()
    serializer_class = serializers.ExamSheetEvalSerializer
    permission_classes = (IsOwner, IsTeacher)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('student', 'grade', 'is_finished')


class StudentGradeViewset(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """Viewset for StudentGrade serialized data"""
    queryset = models.StudentGrade.objects.all()
    serializer_class = serializers.StudentGradeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('student', 'grade')


class TaskToEvaluateViewset(viewsets.ModelViewSet):
    """Viewset for TaskToEvaluate serialized data"""
    queryset = models.TaskToEvaluate.objects.all
    serializer_class = serializers.TaskToEvaluate
