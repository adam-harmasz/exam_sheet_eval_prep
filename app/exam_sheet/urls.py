from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('exams', views.ExamSheetViewset)
router.register('tasks', views.TaskViewset)

app_name = 'exam_sheet'

urlpatterns = [
    path('', include(router.urls))
]
