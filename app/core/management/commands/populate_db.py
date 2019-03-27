from random import randint
from django.core.management.base import BaseCommand


from ... import models
from ... import utils


class Command(BaseCommand):
    """Django command to pause execution until db is available"""

    help = "Populate database"

    def handle(self, *args, **options):
        """Populating database with mocked data"""

        # creating user with is_teacher flag set True
        teacher = models.User.objects.create(
            email=f"teacher{randint(0, 10000)}@teacher.pl",
            first_name="Janusz",
            last_name="Kowalski",
            is_teacher=True,
        )
        # Creating normal user
        student = models.User.objects.create(
            email=f"student{randint(0, 10000)}@student.pl",
            first_name="Andrzej",
            last_name="Nowak",
            is_teacher=False,
        )
        models.ExamSheet.objects.create(
            owner=teacher, name="Exam 1", number_of_copies=2
        )
        models.ExamSheet.objects.create(
            owner=teacher, name="Exam 2", number_of_copies=2
        )
        exams = models.ExamSheet.objects.all()
        # creating tasks and answers for exam
        for exam in exams:
            task1 = models.Task.objects.create(
                owner=teacher,
                exam_sheet=exam,
                name="Task 1",
                question="Question 1 Exam 1",
                points_to_achieve=2,
            )
            task2 = models.Task.objects.create(
                owner=teacher,
                exam_sheet=exam,
                name="Task 2",
                question="Question 2 Exam 1",
                points_to_achieve=2,
            )
            models.Task.objects.create(
                owner=teacher,
                exam_sheet=exam,
                name="Task 3",
                question="Question 3 Exam 1",
                points_to_achieve=10,
                is_open_task=True,
            )
            models.Task.objects.create(
                owner=teacher,
                exam_sheet=exam,
                name="Task 4",
                question="Question 4 Exam 1",
                points_to_achieve=10,
                is_open_task=True,
            )
            for i in range(4):
                if i == 0:
                    models.Answer.objects.create(
                        owner=teacher,
                        answer=f"my answer {i + 1}",
                        task=task1,
                        is_correct=True,
                    )
                    models.Answer.objects.create(
                        owner=teacher,
                        answer=f"my answer {i + 1}",
                        task=task2,
                        is_correct=True,
                    )
                else:
                    models.Answer.objects.create(
                        owner=teacher, answer=f"my answer {i + 1}", task=task1
                    )
                    models.Answer.objects.create(
                        owner=teacher, answer=f"my answer {i + 1}", task=task2
                    )
            exam.is_finished = True
            exam.save()
            # creating ExamSheetForStudent objects based on ExamSheet
            utils.util_create_student_exam(exam)
        student_exams = models.ExamSheetForStudent.objects.all()
        # filling essential data for ExamSheetForStudent objects
        for s_exam in student_exams:
            s_exam.student = student
            tasks = s_exam.student_exam_task.all()
            open_tasks = s_exam.open_exam_task.all()
            for open_task, closed_task in zip(open_tasks, tasks):
                open_task.students_answer = f"My answer {open_task.name}"
                open_task.save()
                id_list = sorted([_.id for _ in closed_task.student_task_answer.all()])
                closed_task.students_answer = randint(id_list[0], id_list[-1])
                closed_task.save()
            s_exam.is_finished = True
            s_exam.save()
            # Creating ExamSheetEvaluation object based on ExamSheetForStudent
            utils.util_create_exam_eval_sheet(s_exam)
        exams_to_eval = models.ExamSheetEvaluation.objects.all()
        # filling essential data for ExamSheetEvaluation objects
        for e_exam in exams_to_eval:
            tasks_to_eval = e_exam.exam_task_eval.all()
            for task in tasks_to_eval:
                task.points_earned = 7
                task.save()
                e_exam.points_earned += task.points_earned
                e_exam.save()
            e_exam.grade = 5
            e_exam.is_finished = True
            e_exam.save()
            # creating StudentGrade object based on ExamSheetEvaluation
            utils.util_create_grade(e_exam)
