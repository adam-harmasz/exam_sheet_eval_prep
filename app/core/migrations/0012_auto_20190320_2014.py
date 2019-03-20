# Generated by Django 2.1.7 on 2019-03-20 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190320_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenTaskForStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('question', models.TextField()),
                ('points_to_achieve', models.IntegerField()),
                ('students_answer', models.TextField(blank=True, null=True)),
                ('exam_sheet_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_exam_task', to='core.ExamSheetForStudent')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='taskforstudent',
            name='is_open_task',
        ),
        migrations.RemoveField(
            model_name='tasktoevaluate',
            name='is_open_task',
        ),
        migrations.AddField(
            model_name='tasktoevaluate',
            name='points_earned',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taskforstudent',
            name='students_answer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]