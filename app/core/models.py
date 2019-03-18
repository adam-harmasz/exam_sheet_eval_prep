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


class ExamSheet(models.Model):
    """Model handling Exam sheet objects"""
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='owner_sheets')
    total_points = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number_of_copies = models.IntegerField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        """String representation of the object"""
        return f'{self.name}'


class Answer(models.Model):
    """Model handling answer objects related to Task objects"""
    task = models.ForeignKey('Task',
                             on_delete=models.CASCADE,
                             related_name='task_answer')
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the object"""
        return f'{self.answer}'


class Task(models.Model):
    """Model handling Task objects"""
    name = models.CharField(max_length=255)
    exam_sheet = models.ForeignKey('ExamSheet',
                                   on_delete=models.CASCADE,
                                   related_name='exam_task')
    question = models.TextField()
    points_to_achieve = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the object"""
        return f'{self.name}'


class ExamSheetForStudent(models.Model):
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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='exam_owner')
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='student_exam',
                                null=True,
                                blank=True,)
    name = models.CharField(max_length=255)
    exam_sheet_origin = models.ForeignKey('ExamSheet',
                                          on_delete=models.CASCADE,
                                          related_name='student_exam_sheet')
    grade = models.IntegerField(choices=EXAM_GRADES, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)


class TaskForStudent(models.Model):
    """Model handling Task objects"""
    name = models.CharField(max_length=255)
    exam_sheet = models.ForeignKey('ExamSheetForStudent',
                                   on_delete=models.CASCADE,
                                   related_name='student_exam_task')
    question = models.TextField()
    students_answer = models.ManyToManyField('AnswerForStudent')
    points_to_achieve = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the object"""
        return f'{self.name}'


class AnswerForStudent(models.Model):
    """Model handling answer objects related to Task objects"""
    task = models.ForeignKey('TaskForStudent',
                             on_delete=models.CASCADE,
                             related_name='task_answer')
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the object"""
        return f'{self.answer}'
