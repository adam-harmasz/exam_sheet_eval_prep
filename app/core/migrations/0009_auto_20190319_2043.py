# Generated by Django 2.1.7 on 2019-03-19 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0008_user_is_teacher")]

    operations = [
        migrations.CreateModel(
            name="ExamSheetEvaluation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("points_to_get", models.IntegerField()),
                ("points_earned", models.IntegerField()),
                (
                    "grade",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, 2),
                            (2, 2.5),
                            (3, 3),
                            (4, 3.5),
                            (5, 4),
                            (6, 4.5),
                            (7, 5),
                        ],
                        null=True,
                    ),
                ),
                ("comment", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="students_exam",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.RemoveField(model_name="examsheetforstudent", name="grade"),
    ]
