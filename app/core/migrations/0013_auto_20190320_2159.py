# Generated by Django 2.1.7 on 2019-03-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190320_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktoevaluate',
            name='points_to_achieve',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]