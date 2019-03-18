from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


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
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class BaseExamSheet(models.Model):
    """Base abstract class for ExamSheet and ExamSheetForStudent models"""
    name = models.CharField(max_length=255)
    total_points = models.IntegerField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        """String representation of the object"""
        return f'{self.name}'


class ExamSheet(BaseExamSheet):
    """Model handling Exam sheet objects"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='owner_sheets')
    number_of_copies = models.IntegerField(null=True, blank=True)


class ExamSheetForStudent(BaseExamSheet):
    """Model to create exam sheets for students objects """
    EXAM_GRADES = (
        (1, 2),
        (2, 2.5),
        (3, 3),
        (4, 3.5),
        (5, 4),
        (6, 4.5),
        (7, 5)
    )
    owner = models.ForeignKey (settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='owner_student_sheets')
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='student_exam',
                                null=True,
                                blank=True,)
    exam_sheet_origin = models.ForeignKey('ExamSheet',
                                          on_delete=models.CASCADE,
                                          related_name='student_exam_sheet')
    grade = models.IntegerField(choices=EXAM_GRADES, null=True, blank=True)


class BaseAnswer(models.Model):
    """Abstract base model for Answer and AnswerForStudent models"""
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        """String representation of the object"""
        return f'{self.answer}'


class Answer(BaseAnswer):
    """Model handling answer objects related to Task objects"""
    task = models.ForeignKey ('Task',
                              on_delete=models.CASCADE,
                              related_name='task_answer',
                              null=True,
                              blank=True)


class AnswerForStudent(BaseAnswer):
    """Model handling answer objects related to Task objects"""
    task = models.ForeignKey ('Task',
                              on_delete=models.CASCADE,
                              related_name='student_task_answer',
                              null=True,
                              blank=True)


class BaseTask(models.Model):
    """Base abstract model for Task and TaskForStudents models"""
    name = models.CharField(max_length=255)
    question = models.TextField()
    points_to_achieve = models.IntegerField()
    created = models.DateTimeField (auto_now_add=True)
    updated = models.DateTimeField (auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        """String representation of the object"""
        return f'{self.name}'


class Task(models.Model):
    """Model handling Task objects"""
    exam_sheet = models.ForeignKey('ExamSheetForStudent',
                                   on_delete=models.CASCADE,
                                   related_name='exam_task')


class TaskForStudent(models.Model):
    """Model handling Task objects"""
    exam_sheet = models.ForeignKey('ExamSheetForStudent',
                                   on_delete=models.CASCADE,
                                   related_name='student_exam_task')
    students_answer = models.CharField(max_length=255)
