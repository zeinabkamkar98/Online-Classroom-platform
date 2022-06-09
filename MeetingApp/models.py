from django.db import models
import uuid
from django.urls import reverse 
# Create your models here.

class User(models.Model):
    user_name=models.CharField(max_length=100,primary_key=True)
    full_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=100)
   
    def __str__(self):
        return self.user_name

class Meeting(models.Model):
    link=models.CharField(max_length=300,primary_key=True,default=uuid.uuid4)
    name=models.CharField(max_length=100)
    description=models.TextField(null=True)

    def __str__(self):
        return self.name

class Umr(models.Model):
    role_type = (
    ('t', 'teacher'),
    ('s', 'student'),
    )
    role= models.CharField(max_length=1, choices=role_type)    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    meeting=models.ForeignKey(Meeting,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.user_name} , {self.role} , {self.meeting.name}'

class Message(models.Model):
    content=models.TextField(null=True)
    sender_name=models.CharField(max_length=100)
    date=models.DateTimeField()
    meeting=models.ForeignKey(Meeting,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sender_name} , {self.meeting.name} '

class Quiz(models.Model):
    name=models.CharField(max_length=100,unique=True)
    begin=models.CharField(max_length=100,null=True)
    end=models.CharField(max_length=100,null=True)
    status=models.BooleanField()
    meeting=models.ForeignKey(Meeting,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} , {self.meeting.name}'

class Question(models.Model):
    number=models.IntegerField()
    content=models.TextField()
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'q{self.number} , {self.quiz.name} , {self.quiz.meeting.name}'

class Answer(models.Model):
    content=models.TextField()
    user=models.CharField(max_length=100)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} , {self.question.number} , {self.question.quiz.name}'