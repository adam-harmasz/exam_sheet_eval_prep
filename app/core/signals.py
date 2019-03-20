from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


def create_exam_sheet_for_student(sender, instance, **kwargs):
    """Signal to create multiple exam sheets"""
    if instance.is_finished:
        tasks = instance.exam_task.all()
        for i in range(instance.number_of_copies):
            exam_sheet_student = models.ExamSheetForStudent.objects.create(
                name=instance.name,
                owner=instance.owner,
                exam_sheet_origin=instance
            )
            for task in tasks:
                answers = task.task_answer.all()
                task_for_student = models.TaskForStudent.objects.create(
                    name=task.name,
                    question=task.question,
                    points_to_achieve=task.points_to_achieve,
                    exam_sheet_student=exam_sheet_student
                )
                for answer in answers:
                    models.AnswerForStudent.objects.create(
                        task=task_for_student,
                        answer=answer.answer,
                        is_correct=answer.is_correct
                    )


def create_exam_eval(sender, instance, **kwargs):
    """Creating ExamEval object if ExamSheetForStudent is finished"""
    if instance.is_finished:
        tasks = instance.student_exam_task.all()
        student = instance.student
        owner = instance.owner
        # sum of maximum points available to get
        points_to_get = sum(task.points_to_achieve for task in tasks)
        points_earned = 0
        for task2 in tasks:
            answer_id = int(task2.students_answer)
            students_answer = models.AnswerForStudent.objects.get(pk=answer_id)
            # if asnwer is correct add points
            if students_answer.is_correct:
                points_earned += task2.points_to_achieve
        # create ExamSheetEvaluation object based on student sheet
        models.ExamSheetEvaluation.objects.create(
            owner=owner,
            student=student,
            points_to_get=points_to_get,
            points_earned=points_earned
        )


def create_grade(sender, instance, **kwargs):
    """Create Grade object and assign to student when exam sheet evaluation is done"""
    if instance.is_finished:
        print('JESTEM W CREATE GRADE')
        owner = instance.owner
        student = instance.student
        grade = instance.grade
        exam = instance
        student_grade = models.StudentGrade.objects.filter(exam=exam)
        if student_grade.exists():
            student_grade.update(
                owner=owner,
                student=student,
                grade=grade,
                exam=exam
            )
        else:
            models.StudentGrade.objects.create(
                owner=owner,
                student=student,
                grade=grade,
                exam=exam
            )
