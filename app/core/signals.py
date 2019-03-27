from . import utils


def create_exam_sheet_for_student(sender, instance, **kwargs):
    """Signal to create multiple exam sheets"""
    utils.util_create_student_exam(instance)


def create_exam_eval(sender, instance, **kwargs):
    """Creating ExamEval object if ExamSheetForStudent is finished"""
    utils.util_create_exam_eval_sheet(instance)


def create_grade(sender, instance, **kwargs):
    """Create Grade object and assign to student when exam sheet evaluation is done"""
    utils.util_create_grade(instance)
