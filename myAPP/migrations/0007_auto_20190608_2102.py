# Generated by Django 2.1.7 on 2019-06-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAPP', '0006_auto_20190608_1939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departments',
            name='director_id',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='arrange_id',
        ),
        migrations.AddField(
            model_name='departments',
            name='employee_id',
            field=models.IntegerField(default=0),
        ),
    ]