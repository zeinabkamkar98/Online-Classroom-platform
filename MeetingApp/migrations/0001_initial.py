# Generated by Django 3.0.8 on 2020-07-21 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('link', models.CharField(max_length=300, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Umr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('o', 'owner'), ('s', 'student')], max_length=1)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MeetingApp.Meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MeetingApp.User')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('begin', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('state', models.BooleanField()),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MeetingApp.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('content', models.TextField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MeetingApp.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sender_name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MeetingApp.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('user', models.CharField(max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MeetingApp.Question')),
            ],
        ),
    ]
