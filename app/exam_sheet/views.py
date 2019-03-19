from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwner
from . import serializers
from core import models


class ExamSheetViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheet objects"""
    queryset = models.ExamSheet.objects.all()
    serializer_class = serializers.ExamSheetSerializer
    permission_classes = (IsOwner,)

    def get_serializer_context(self):
        return {'request': self.request}


class TaskViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsOwner,)

    def get_serializer_context(self):
        return {'request': self.request}


class AnswerViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = (IsOwner,)

    def get_serializer_context(self):
        return {'request': self.request}
