from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.loginpage,name='loginpage'),
    path('user_login',views.user_login,name='user_login'),
    path('logout',views.logout,name='logout'),

    path('adminpanel',views.adminpanel,name='adminpanel'),
    path('userdetails',views.userdetails,name='userdetails'),

    path('teacherregister',views.teacherregister,name='teacherregister'),
    path('register_teacher',views.register_teacher,name='register_teacher'),
    path('teacher/<int:pk>',views.teacher_home,name='teacher_home'),
    path('resetpage',views.resetpage,name='resetpage'),
    path('reset',views.reset,name='reset'),

    path('studentregister',views.studentregister,name='studentregister'),
    path('register_student',views.register_student,name='register_student'),
    path('student/<int:pk>',views.student_home,name='student_home'),

    path('approve/<int:pk>',views.approve,name='approve'),
    path('disapprove/<int:pk>',views.disapprove,name='disapprove'),


]