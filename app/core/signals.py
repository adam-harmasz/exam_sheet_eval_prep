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
                if task.is_open_task:
                    models.OpenTaskForStudent.objects.create(
                        name=task.name,
                        question=task.question,
                        points_to_achieve=task.points_to_achieve,
                        exam_sheet_student=exam_sheet_student
                    )
                else:
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
        open_tasks = instance.open_exam_task.all()
        student = instance.student
        owner = instance.owner
        # sum of maximum points available to get
        points_to_get = sum(task.points_to_achieve for task in tasks)
        points_earned = 0
        for task_ in tasks:
            answer_id = int(task_.students_answer)
            students_answer = models.AnswerForStudent.objects.get(pk=answer_id)
            # if answer is correct add points
            if students_answer.is_correct:
                points_earned += task_.points_to_achieve
        # create ExamSheetEvaluation object based on student sheet
        exam = models.ExamSheetEvaluation.objects.create(
            owner=owner,
            student=student,
            points_to_get=points_to_get,
            points_earned=points_earned
        )
        # create TaskToEvaluate objects based on OpenTask objects
        if open_tasks:
            for open_task in open_tasks:
                models.TaskToEvaluate.objects.create(
                    owner=open_task.owner,
                    question=open_task.question,
                    points_to_achieve=open_task.points_to_achieve,
                    students_answer=open_task.students_answer,
                    exam=exam
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
