from rest_framework import viewsets, mixins
from django_filters import rest_framework as filters

from . import serializers
from core import models


class ExamSheetForStudentViewset(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for ExamSheet objects"""

    queryset = models.ExamSheetForStudent.objects.all()
    serializer_class = serializers.ExamSheetForStudentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name", "student_exam_task", "is_finished", "owner")

    def get_serializer_context(self):
        # print(self.get_object(), 'obiekt w viewset')
        return {"request": self.request}


class TaskForStudentViewset(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for Task objects"""

    queryset = models.TaskForStudent.objects.all()
    serializer_class = serializers.TaskForStudentSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class OpenTaskForStudentViewset(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for Task objects"""

    queryset = models.OpenTaskForStudent.objects.all()
    serializer_class = serializers.OpenTaskForStudentSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class AnswerForStudentViewset(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for Task objects"""

    queryset = models.AnswerForStudent.objects.all()
    serializer_class = serializers.AnswerForStudentSerializer

    def get_serializer_context(self):
        return {"request": self.request}
