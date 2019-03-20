from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwner, IsTeacher
from . import serializers
from core import models


class ExamSheetViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheet objects"""
    serializer_class = serializers.ExamSheetSerializer
    permission_classes = (IsOwner, IsTeacher)

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        """Allow users to see only objects created by them, except superuser"""
        if self.request.user.is_superuser:
            return models.ExamSheet.objects.all()
        elif self.request.user.is_teacher:
            return models.ExamSheet.objects.filter(id=self.request.user.id)


class TaskViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsOwner, IsTeacher)

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Task.objects.all()
        elif self.request.user.is_teacher:
            return models.Task.objects.filter(id=self.request.user.id)


class AnswerViewset(viewsets.ModelViewSet):
    """Viewset for Task objects"""
    serializer_class = serializers.AnswerSerializer
    permission_classes = (IsOwner, IsTeacher)

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Answer.objects.all()
        elif self.request.user.is_teacher:
            return models.Answer.objects.filter(id=self.request.user.id)
