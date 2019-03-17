from rest_framework import viewsets

from .serializers import ExamSheetSerializer
from core import models


class ExamSheetViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheet objects"""
    queryset = models.ExamSheet.objects.all()
    serializer_class = ExamSheetSerializer
