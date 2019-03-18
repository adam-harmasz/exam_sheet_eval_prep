from rest_framework import viewsets

from . import serializers
from core import models


class ExamSheetViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheet objects"""
    queryset = models.ExamSheet.objects.all()
    serializer_class = serializers.ExamSheetSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class TaskViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class AnswerViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer

    def get_serializer_context(self):
        return {'request': self.request}
