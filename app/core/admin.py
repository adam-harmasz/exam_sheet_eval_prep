from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "first_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_teacher", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.ExamSheet)
admin.site.register(models.Task)
admin.site.register(models.Answer)
admin.site.register(models.ExamSheetForStudent)
admin.site.register(models.TaskForStudent)
admin.site.register(models.AnswerForStudent)
admin.site.register(models.ExamSheetEvaluation)
admin.site.register(models.StudentGrade)
admin.site.register(models.TaskToEvaluate)
