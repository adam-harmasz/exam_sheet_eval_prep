# Generated by Django 2.1.7 on 2019-03-17 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190317_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
