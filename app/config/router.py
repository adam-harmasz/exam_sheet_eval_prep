from rest_framework.routers import DefaultRouter
from django.urls import path, include

from exam_eval import views as exam_eval_views
from exam_sheet import views as exam_sheet_views
from exam_sheet_student import views as student_views

router = DefaultRouter()
router.register(
    'exam_eval', exam_eval_views.ExamSheetEvalViewset, base_name='exam_eval')
router.register(
    'student_grade', exam_eval_views.StudentGradeViewset, base_name='student_grade')
router.register(
    'exam_sheets', exam_sheet_views.ExamSheetViewset, base_name='exam')
router.register(
    'task_sheets', exam_sheet_views.TaskViewset, base_name='task')
router.register(
    'answer_sheets', exam_sheet_views.AnswerViewset, base_name='answer')
router.register(
    'exam_student', student_views.ExamSheetForStudentViewset, base_name='exam_student')
router.register(
    'task_student', student_views.TaskForStudentViewset, base_name='task_student')
router.register(
    'answer_student', student_views.AnswerForStudentViewset, base_name='answer_student')

urlpatterns = [
    path('api/v1/', include(router.urls))
]
