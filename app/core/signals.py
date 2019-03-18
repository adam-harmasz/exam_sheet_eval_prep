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
    else:
        pass
