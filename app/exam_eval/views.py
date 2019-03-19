from rest_framework import viewsets, mixins

from exam_sheet.permissions import IsOwner, IsTeacher
from . import serializers
from core import models


class ExamSheetEvalViewset(viewsets.ModelViewSet):
    """Viewset for ExamSheetEvaluation serialized data"""
    queryset = models.ExamSheetEvaluation.objects.all()
    serializer_class = serializers.ExamSheetEvalSerializer
    permission_classes = (IsOwner,)
