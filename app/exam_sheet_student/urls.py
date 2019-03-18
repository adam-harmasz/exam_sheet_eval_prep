from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('exams', views.ExamSheetForStudentViewset, base_name='exam_student')
router.register('tasks', views.TaskForStudentViewset, base_name='task_student')
router.register('answers', views.AnswerForStudentViewset, base_name='answer_student')

app_name = 'exam_sheet_student'

urlpatterns = [
    path('', include(router.urls)),
]
