from rest_framework import viewsets, mixins

from . import serializers
from core import models


class ExamSheetForStudentViewset(mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    """Viewset for ExamSheet objects"""
    queryset = models.ExamSheetForStudent.objects.all()
    serializer_class = serializers.ExamSheetForStudentSerializer

    def get_serializer_context(self):
        # print(self.get_object(), 'obiekt w viewset')
        return {'request': self.request}


class TaskForStudentViewset(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Viewset for Task objects"""
    queryset = models.TaskForStudent.objects.all()
    serializer_class = serializers.TaskForStudentSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class AnswerForStudentViewset(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """Viewset for Task objects"""
    queryset = models.AnswerForStudent.objects.all()
    serializer_class = serializers.AnswerForStudentSerializer

    def get_serializer_context(self):
        return {'request': self.request}
