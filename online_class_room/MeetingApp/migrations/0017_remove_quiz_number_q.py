# Generated by Django 3.0.8 on 2020-07-27 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MeetingApp', '0016_quiz_number_q'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='number_q',
        ),
    ]