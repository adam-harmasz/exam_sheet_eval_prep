from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register("exams", views.ExamSheetViewset, base_name="exam")
router.register("tasks", views.TaskViewset, base_name="task")
router.register("answers", views.AnswerViewset, base_name="answer")

app_name = "exam_sheet"

urlpatterns = [path("", include(router.urls))]
