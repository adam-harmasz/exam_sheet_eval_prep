from rest_framework import viewsets

from . import serializers
from core import models


class ExamSheetForStudentViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheet objects"""
    queryset = models.ExamSheet.objects.all()
    serializer_class = serializers.ExamSheetForStudentSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class TaskForStudentViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskForStudentSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class AnswerForStudentViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerForStudentSerializer

    def get_serializer_context(self):
        return {'request': self.request}
