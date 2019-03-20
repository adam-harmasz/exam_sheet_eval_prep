from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.db.models.signals import post_save

from . import signals


class UserManager(BaseUserManager):
    """class to manage Abstract User objects"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new User"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Creates and saves new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_teacher = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class BaseModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class BaseExamSheet(BaseModel):
    """Base abstract class for ExamSheet and ExamSheetForStudent models"""
    name = models.CharField(max_length=255)
    total_points = models.IntegerField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        """String representation of the object"""
        return f'{self.name}'


class ExamSheet(BaseExamSheet):
    """Model handling Exam sheet objects"""
    number_of_copies = models.IntegerField(null=True, blank=True)


class ExamSheetForStudent(BaseExamSheet):
    """Model to create exam sheets for students objects """
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='student_exam',
                                null=True,
                                blank=True,)
    exam_sheet_origin = models.ForeignKey('ExamSheet',
                                          on_delete=models.CASCADE,
                                          related_name='student_exam_sheet')


class BaseAnswer(BaseModel):
    """Abstract base model for Answer and AnswerForStudent models"""
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        """String representation of the object"""
        return f'{self.answer}'


class Answer(BaseAnswer):
    """Model handling answer objects related to Task objects"""
    task = models.ForeignKey('Task',
                              on_delete=models.CASCADE,
                              related_name='task_answer',
                              null=True,
                              blank=True)


class AnswerForStudent(BaseAnswer):
    """Model handling answer objects related to Task objects"""
    task = models.ForeignKey('TaskForStudent',
                              on_delete=models.CASCADE,
                              related_name='student_task_answer',
                              null=True,
                              blank=True)


class BaseTask(BaseModel):
    """Base abstract model for Task and TaskForStudents models"""
    name = models.CharField(max_length=255)
    question = models.TextField()
    points_to_achieve = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        """String representation of the object"""
        return f'{self.name}'


class Task(BaseTask):
    """Model handling Task objects"""
    exam_sheet = models.ForeignKey('ExamSheet',
                                   on_delete=models.CASCADE,
                                   related_name='exam_task')
    is_open_task = models.BooleanField(default=False)


class TaskForStudent(BaseTask):
    """Model handling TaskForStudent objects"""
    exam_sheet_student = models.ForeignKey('ExamSheetForStudent',
                                           on_delete=models.CASCADE,
                                           related_name='student_exam_task')
    students_answer = models.IntegerField(null=True, blank=True)


class OpenTaskForStudent(BaseTask):
    """Model handling TaskForStudent objects"""
    exam_sheet_student = models.ForeignKey('ExamSheetForStudent',
                                            on_delete=models.CASCADE,
                                            related_name='open_exam_task')
    students_answer = models.TextField(null=True, blank=True)


class ExamSheetEvaluation(BaseModel):
    """Model handling ExamSheetEvaluation objects"""
    EXAM_GRADES = (
        (1, 2),
        (2, 2.5),
        (3, 3),
        (4, 3.5),
        (5, 4),
        (6, 4.5),
        (7, 5)
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='students_exam')
    points_to_get = models.IntegerField()
    points_earned = models.IntegerField()
    score_in_percents = models.FloatField(null=True, blank=True)
    grade = models.IntegerField(choices=EXAM_GRADES, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        """String representation of the object"""
        return f'Exam evaluation - {self.student}'


class TaskToEvaluate(BaseTask):
    """Model handling TaskToEvaluate objects"""
    students_answer = models.TextField()
    points_to_achieve = models.IntegerField(null=True, blank=True)
    points_earned = models.IntegerField(null=True, blank=True)
    exam = models.ForeignKey('ExamSheetEvaluation',
                             on_delete=models.CASCADE,
                             related_name='exam_task_eval')


class StudentGrade(BaseModel):
    """Model handling StudentGrade objects"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='student_grade')
    grade = models.FloatField()
    exam = models.OneToOneField('ExamSheetEvaluation', on_delete=models.CASCADE)

    def __str__(self):
        """String representation of the object"""
        return f'{self.student} grade: {self.grade}'


# creating ExamSheetForStudent objects
post_save.connect(signals.create_exam_sheet_for_student, sender=ExamSheet)
# creating ExamEvaluation object
post_save.connect(signals.create_exam_eval, sender=ExamSheetForStudent)
# creating StudentGrade object
post_save.connect(signals.create_grade, sender=ExamSheetEvaluation)
