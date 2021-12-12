from django.urls import re_path as url
from django.urls import path

from . import views

app_name='MeetingApp'

urlpatterns = [
    url(r'^$',views.index,name='index'),


    url(r'^sign_in_page/$',views.sign_in_page,name='sign_in_page'),
    url(r'^sign_up_page/$',views.sign_up_page,name='sign_up_page'),
    url(r'^sign_up/$',views.sign_up,name='sign_up'),
    url(r'^sign_in/$',views.sign_in,name='sign_in'),


    url(r'^join_class/$',views.join_class,name='join_class'),    
    url(r'^join_class_page/$',views.join_class_page,name='join_class_page'),
    url(r'^create_class_page/$',views.create_class_page,name='create_class_page'),
    url(r'^create_class/$',views.create_class,name='create_class'),


    url(r'^single_meeting/(?P<meeting_link>[a-z0-9-_]*)/$',views.single_meeting,name='single_meeting'), 
    url(r'^join_meeting/(?P<meeting_link>[a-z0-9-_]*)/$',views.join_meeting,name='join_meeting'),

    url(r'^send_message/(?P<meeting_link>[a-z0-9-_]*)/$',views.send_message,name='send_message'),
    url(r'^refresh_message/(?P<meeting_link>[a-z0-9-_]*)/$',views.refresh_message,name='refresh_message'),


    url(r'^add_teacher_page/(?P<meeting_link>[a-z0-9-_]*)/$',views.add_teacher_page,name='add_teacher_page'),
    url(r'^add_teacher/(?P<meeting_link>[a-z0-9-_]*)/$',views.add_teacher,name='add_teacher'),


    url(r'^add_student_page/(?P<meeting_link>[a-z0-9-_]*)/$',views.add_student_page,name='add_student_page'),
    url(r'^add_student/(?P<meeting_link>[a-z0-9-_]*)/$',views.add_student,name='add_student'),


    url(r'^add_quiz/(?P<meeting_link>[a-z0-9-_]*)/$',views.add_quiz,name='add_quiz'),
    url(r'^add_quiz_page/(?P<meeting_link>[a-z0-9-_]*)/$',views.add_quiz_page,name='add_quiz_page'),

    url(r'^add_questions/(?P<quiz_id>[a-z0-9-_]*)/$',views.add_questions,name='add_questions'),

    url(r'^change_status/(?P<quiz_id>[a-z0-9-_]*)/$',views.change_status,name='change_status'),

    url(r'^answer_quiz_page/(?P<quiz_id>[a-z0-9-_]*)/$',views.answer_quiz_page,name='answer_quiz_page'),
    url(r'^answer_quiz/(?P<quiz_id>[a-z0-9-_]*)/$',views.answer_quiz,name='answer_quiz'),
    
    url(r'^quiz_result/(?P<quiz_id>[a-z0-9-_]*)/$',views.quiz_result,name='quiz_result'),
    url(r'^student_quiz_result/(?P<quiz_id>[a-z0-9-_]*)/(?P<user>[a-z0-9-_]*)/$',views.student_quiz_result,name='student_quiz_result'),

    url(r'^left_meeting/(?P<meeting_link>[a-z0-9-_]*)/$',views.left_meeting,name='left_meeting'),
    url(r'^delete_meeting/(?P<meeting_link>[a-z0-9-_]*)/$',views.delete_meeting,name='delete_meeting'),

    url(r'^delete_teacher/(?P<meeting_link>[a-z0-9-_]*)/(?P<user_name>[a-z0-9-_]*)/$',views.delete_teacher,name='delete_teacher'),
    url(r'^delete_student/(?P<meeting_link>[a-z0-9-_]*)/(?P<user_name>[a-z0-9-_]*)/$',views.delete_student,name='delete_student'),
    url(r'^delete_quiz/(?P<meeting_link>[a-z0-9-_]*)/(?P<quiz_id>[a-z0-9-_]*)/$',views.delete_quiz,name='delete_quiz'),



]
