from rest_framework import viewsets

from . import serializers
from core import models


class ExamSheetViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheet objects"""
    queryset = models.ExamSheet.objects.all()
    serializer_class = serializers.ExamSheetSerializer


class TaskViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer


class AnswerViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
