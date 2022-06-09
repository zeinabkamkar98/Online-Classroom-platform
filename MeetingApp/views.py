from django.shortcuts import render
from django.http import HttpResponse
from . import models
from datetime import datetime

# Create your views here.
#######################################################
def index(request):
    return render(request, 'MeetingApp/index.html', {})

def join_meeting(request):
    return render(request, 'MeetingApp/student_meeting.html', {})

#######################################################
def sign_in_page(request):
    return render(request, 'MeetingApp/sign_in.html', {})


def sign_up_page(request):
    return render(request, 'MeetingApp/sign_up.html', {})


def sign_up(request):  

    user_name=request.POST["user_name"]
    email=request.POST["email"]
    e_user_name=models.User.objects.all().filter(user_name=user_name).count()
    e_email=models.User.objects.all().filter(email=email).count()

    username_error=""
    email_error=""
    password_error=""
    if(e_user_name!=0):
        username_error="try another user_name."
    if(e_email!=0):
        email_error="try another email"
    if(request.POST["password1"]==request.POST["password2"]):
        password_error="password didn't match."
    if(e_user_name==0 and e_email==0 and request.POST["password1"]==request.POST["password2"]):
        new_user=models.User(full_name=request.POST["full_name"],user_name=user_name,email=email,password=request.POST["password1"])
        new_user.save()
        request.session["user_name"]=new_user.user_name
        return render(request, 'MeetingApp/classes.html')
    else:
        return render(request, 'MeetingApp/sign_up.html', {"username_error":username_error,"email_error":email_error,"password_error":password_error})


def sign_in(request):

    name=request.POST["name"]
    password=request.POST["password"]
    user_name=models.User.objects.all().filter(user_name=name).count()
    email=models.User.objects.all().filter(email=name).count()

    if(user_name==0 and email==0):
        return render(request, 'MeetingApp/sign_in.html', {"error":"username(email) or password is wrong."})

    elif (email==0):
        user=models.User.objects.get(user_name=name)
        if(user.password==password):
            umr=user.umr_set.all()
            request.session["user_name"]=user.user_name
            return render(request, 'MeetingApp/classes.html',{"classes":umr})
        else:
            return render(request, 'MeetingApp/sign_in.html',  {"error":"username(email) or password is wrong."})

    else:
        user=models.User.objects.get(email=name)
        if(user.password==password):
            umr=user.umr_set.all()
            request.session["user_name"]=user.user_name
            return render(request, 'MeetingApp/classes.html',{"classes":umr})
        else:
            return render(request, 'MeetingApp/sign_in.html',  {"error":"username(email) or password is wrong."})


###########################################################################
def single_meeting(request,meeting_link):
    meeting=models.Meeting.objects.get(link=meeting_link)
    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    quizes=meeting.quiz_set.all()
    urm=meeting.umr_set.filter(user__user_name=request.session["user_name"])[0]

    if(urm.role=='student'):
        return render(request, 'MeetingApp/single_class_student.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})
    else:
        return render(request, 'MeetingApp/single_class_teacher.html' ,{"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})



#############################################################################
def join_class_page(request):
    return render(request, 'MeetingApp/join_class.html', {})

def join_class(request):

    link=request.POST["link"]
    count=models.Meeting.objects.filter(link=link).count()

    if(count!=0):
        
        meeting=models.Meeting.objects.get(link=link)
        students=meeting.umr_set.filter(user=request.session["user_name"]).filter(role="student").count()

        if(students==0):

            user=models.User.objects.get(user_name=request.session["user_name"])
            umr=models.Umr(user=user,meeting=meeting,role='student')
            umr.save()
            umr=user.umr_set.all()
            return render(request, 'MeetingApp/classes.html',{"classes":umr})

        else:

            return render(request, 'MeetingApp/join_class.html', {"error":"you are a student of this class noe."})

    else:
        return render(request, 'MeetingApp/join_class.html', {"error":"there is no class with this link."})


def create_class_page(request):
    return render(request, 'MeetingApp/create_class.html', {})

def create_class(request):
    meeting=models.Meeting(name=request.POST["name"],description=request.POST["description"])
    meeting.save()
    user=models.User.objects.get(user_name=request.session["user_name"])
    umr=models.Umr(user=user,meeting=meeting,role='teacher')
    umr.save()
    umr=user.umr_set.all()
    return render(request, 'MeetingApp/classes.html',{"classes":umr})


#############################################################################
def add_student_page(request,meeting_link):
    return render(request, 'MeetingApp/add_student.html',{"meeting_link":meeting_link})


def add_student(request,meeting_link):
    name=request.POST["name"]
    meeting=models.Meeting.objects.get(link=meeting_link)
    user_name=models.User.objects.all().filter(user_name=name).count()
    email=models.User.objects.all().filter(email=name).count()

    if(user_name==0 and email==0):
        return render(request, 'MeetingApp/add_student.html', {"error":"there is no one with this user or email","meeting_link":meeting_link})

    elif (email==0):
        user=models.User.objects.get(user_name=name)
        students=meeting.umr_set.filter(user=name).filter(role="student").count()
        if students==0:
            umr=models.Umr(user=user,meeting=meeting,role='student')
            umr.save()
            teachers=meeting.umr_set.filter(role='teacher')
            students=meeting.umr_set.filter(role='student')
            quizes=meeting.quiz_set.all()
            return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})
        else:
            return render(request, 'MeetingApp/add_student.html', {"error":"this user is already in this class.","meeting_link":meeting_link})

    else:
        user=models.User.objects.get(email=name)
        students=meeting.umr_set.filter(user=user.user_name).filter(role="student").count()
        if students==0:
            umr=models.Umr(user=user,meeting=meeting,role='student')
            umr.save()
            teachers=meeting.umr_set.filter(role='teacher')
            students=meeting.umr_set.filter(role='student')
            quizes=meeting.quiz_set.all()
            return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})
        else:
            return render(request, 'MeetingApp/add_student.html', {"error":"this user is already in this class.","meeting_link":meeting_link})



#############################################################################
def add_teacher_page(request,meeting_link):
    return render(request, 'MeetingApp/add_teacher.html',{"meeting_link":meeting_link})




def add_teacher(request,meeting_link):
    name=request.POST["name"]
    meeting=models.Meeting.objects.get(link=meeting_link)
    user_name=models.User.objects.all().filter(user_name=name).count()
    email=models.User.objects.all().filter(email=name).count()

    if(user_name==0 and email==0):
        return render(request, 'MeetingApp/add_teacher.html', {"error":"there is no one with this user or email","meeting_link":meeting_link})

    elif (email==0):
        user=models.User.objects.get(user_name=name)
        students=meeting.umr_set.filter(user=name).filter(role="teacher").count()
        if students==0:
            umr=models.Umr(user=user,meeting=meeting,role='teacher')
            umr.save()
            teachers=meeting.umr_set.filter(role='teacher')
            students=meeting.umr_set.filter(role='student')
            quizes=meeting.quiz_set.all()
            return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})
        else:
            return render(request, 'MeetingApp/add_student.html', {"error":"this user is already in this class.","meeting_link":meeting_link})

 
    else:
        user=models.User.objects.get(email=name)
        students=meeting.umr_set.filter(user=user.user_name).filter(role="teacher").count()
        if students==0:
            umr=models.Umr(user=user,meeting=meeting,role='teacher')
            umr.save()
            teachers=meeting.umr_set.filter(role='teacher')
            students=meeting.umr_set.filter(role='student')
            quizes=meeting.quiz_set.all()
            return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})
        else:
            return render(request, 'MeetingApp/add_student.html', {"error":"this user is already in this class.","meeting_link":meeting_link})


###############################################################################
def add_quiz(request,meeting_link):
    meeting=models.Meeting.objects.get(link=meeting_link)
    name=request.POST["name"]
    begin=request.POST["begin"]
    end=request.POST["end"]
    number=request.POST["number"]  
    quiznum=models.Quiz.objects.filter(name=name).count()
    if(quiznum==0):
        quiz=models.Quiz(name=name,meeting=meeting,begin=begin,end=end,status=False)
        quiz.save()
        numItems = range(1, int(number)+1)
        return render(request, 'MeetingApp/add_questions.html', {"meeting_link":meeting_link,"quiz_id":name,"number_q":numItems})
    else:
        return render(request, 'MeetingApp/add_quiz.html',{"meeting_link":meeting_link,"error":"please try another name."})


def add_quiz_page(request,meeting_link):
    return render(request, 'MeetingApp/add_quiz.html',{"meeting_link":meeting_link})




def add_questions(request,quiz_id):
    quiz=models.Quiz.objects.filter(name=quiz_id)[0]
    number=request.POST["i"]

    for i in range(1, int(number)+1):
        content=request.POST["q"+str(i)]
        question=models.Question(content=content,number=i,quiz=quiz)
        question.save()
    
    meeting=quiz.meeting
    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    quizes=meeting.quiz_set.all()
    return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})

################################################################################

def change_status(request,quiz_id):
    quiz=models.Quiz.objects.filter(name=quiz_id)[0]
    
    if(quiz.status==False):
        quiz.status=True
    else:
        quiz.status=False
    
    quiz.save()
    meeting=quiz.meeting
    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    quizes=meeting.quiz_set.all()
    return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})



################################################################################
def answer_quiz_page(request,quiz_id):
    quiz=models.Quiz.objects.filter(name=quiz_id)[0]
    questions=quiz.question_set.all()
    quiz=models.Quiz.objects.filter(name=quiz_id)[0]
    question=quiz.question_set.all()[0]
    students=question.answer_set.filter(user=request.session["user_name"]).count()
    
    if quiz.status==True and students==0:
        return render(request, 'MeetingApp/answer_quiz.html',{"questions":questions,"quiz_id":quiz_id})
 
    else:
        meeting=quiz.meeting
        teachers=meeting.umr_set.filter(role='teacher')
        students=meeting.umr_set.filter(role='student')
        quizes=meeting.quiz_set.all()
        return render(request, 'MeetingApp/single_class_student.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})


def answer_quiz(request,quiz_id):
    quiz=models.Quiz.objects.filter(name=quiz_id)[0]
    questions=quiz.question_set.all()
    user_name=request.session["user_name"]

    
    for question in questions:
        content=request.POST["a"+str(question.number)]
        answer=models.Answer(content=content,question=question,user=user_name)
        answer.save()

    meeting=quiz.meeting
    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    quizes=meeting.quiz_set.all()
    return render(request, 'MeetingApp/single_class_student.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})


def quiz_result(request,quiz_id):
    quiz=models.Quiz.objects.filter(name=quiz_id)[0]
    question=quiz.question_set.all()[0]
    students=question.answer_set.all()
    return render(request, 'MeetingApp/quiz_result.html', {"students":students,"quiz_id":quiz.name})

def student_quiz_result(request,quiz_id,user):
    quiz=models.Quiz.objects.filter(name=quiz_id)[0]
    questions=quiz.question_set.all()
    student_answer=[]

    for question in questions:
        answer=question.answer_set.filter(user=user)
        student_answer.append(answer)
    
    return render(request, 'MeetingApp/student_quiz_result.html', {"answers":student_answer,"quiz_id":quiz.name,"user":user})
#######################################################################################

def join_meeting(request,meeting_link):
    meeting=models.Meeting.objects.get(link=meeting_link)
    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    messages=meeting.message_set.all()
    urm=meeting.umr_set.filter(user__user_name=request.session["user_name"])[0]

    if(urm.role=='student'):
        return render(request, 'MeetingApp/student_meeting.html', {"teachers":teachers,"students":students,"messages":messages,"meeting":meeting})
    else:
        return render(request, 'MeetingApp/teacher_meeting.html' ,{"teachers":teachers,"students":students,"messages":messages,"meeting":meeting})


#######################################################################################
def send_message(request,meeting_link):

    meeting=models.Meeting.objects.get(link=meeting_link)
    content=request.POST["content"]
    sender_name=request.session["user_name"]
    date=datetime.now()

    m=models.Message(content=content,meeting=meeting,sender_name=sender_name,date=date)
    m.save()
    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    messages=meeting.message_set.all()
    urm=meeting.umr_set.filter(user__user_name=request.session["user_name"])[0]
    urm=meeting.umr_set.filter(user__user_name=request.session["user_name"])[0]

    if(urm.role=='student'):
        return render(request, 'MeetingApp/student_meeting.html', {"teachers":teachers,"students":students,"messages":messages,"meeting":meeting})
    else:
        return render(request, 'MeetingApp/teacher_meeting.html' ,{"teachers":teachers,"students":students,"messages":messages,"meeting":meeting})


def refresh_message(request,meeting_link):

    meeting=models.Meeting.objects.get(link=meeting_link)
    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    messages=meeting.message_set.all()
    urm=meeting.umr_set.filter(user__user_name=request.session["user_name"])[0]

    if(urm.role=='student'):
        return render(request, 'MeetingApp/student_meeting.html', {"teachers":teachers,"students":students,"messages":messages,"meeting":meeting})
    else:
        return render(request, 'MeetingApp/teacher_meeting.html' ,{"teachers":teachers,"students":students,"messages":messages,"meeting":meeting})



############################################################################
def delete_student(request,meeting_link,user_name):

    meeting=models.Meeting.objects.get(link=meeting_link)
    meeting.umr_set.filter(user=user_name).filter(role='student').delete()

    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    quizes=meeting.quiz_set.all()
    return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})

def delete_teacher(request,meeting_link,user_name):

    meeting=models.Meeting.objects.get(link=meeting_link)
    meeting.umr_set.filter(user=user_name).filter(role='teacher').delete()

    if user_name==request.session["user_name"]:
        user=models.User.objects.get(user_name=request.session["user_name"])
        umr=user.umr_set.all()
        return render(request, 'MeetingApp/classes.html',{"classes":umr}) 

    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    quizes=meeting.quiz_set.all()
 
    return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})

def delete_quiz(request,meeting_link,quiz_id):

    meeting=models.Meeting.objects.get(link=meeting_link)
    meeting.quiz_set.filter(name=quiz_id).delete()

    teachers=meeting.umr_set.filter(role='teacher')
    students=meeting.umr_set.filter(role='student')
    quizes=meeting.quiz_set.all()
    return render(request, 'MeetingApp/single_class_teacher.html', {"teachers":teachers,"students":students,"quizes":quizes,"meeting":meeting})



def left_meeting(request,meeting_link):

    meeting=models.Meeting.objects.get(link=meeting_link)
    meeting.umr_set.filter(user=request.session["user_name"]).filter(role='student').delete()

    user=models.User.objects.get(user_name=request.session["user_name"])
    umr=user.umr_set.all()
    return render(request, 'MeetingApp/classes.html',{"classes":umr}) 
        
 
def delete_meeting(request,meeting_link):

    meeting=models.Meeting.objects.get(link=meeting_link).delete()

    user=models.User.objects.get(user_name=request.session["user_name"])
    umr=user.umr_set.all()
    return render(request, 'MeetingApp/classes.html',{"classes":umr}) 
      