# Generated by Django 3.0.8 on 2020-07-27 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MeetingApp', '0015_auto_20200727_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='number_q',
            field=models.IntegerField(null=True),
        ),
    ]
