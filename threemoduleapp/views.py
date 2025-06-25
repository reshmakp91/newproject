from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login,authenticate
from threemoduleapp.models import Teacher,CustomUser,Student
import random
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.hashers import check_password

def home(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request,'login.html')

def adminpanel(request):
    if request.user.is_authenticated and request.user.is_staff:
        unapproved = CustomUser.objects.filter(status=0).count()
        num = unapproved-1
        return render(request, 'adminpanel.html',{'num':num})
    else:
        messages.info(request, "Access denied. Only admin can view this page.")
        return redirect('home')
    
def userdetails(request):
    if request.user.is_authenticated and request.user.is_staff:
        users = CustomUser.objects.filter(is_staff=False)
        unapproved = CustomUser.objects.filter(status=0).count()
        num = unapproved-1
        return render(request, 'userdetails.html',{'users':users,'num':num})
    else:
        messages.info(request, "Access denied. Only admin can view this page.")
        return redirect('home')


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.user_type == '1':
                login(request,user)
                messages.info(request,f'Hi, You are now logged in as {request.user.username}')
                return redirect('adminpanel')
            elif user.user_type == '2':
                login(request,user)
                messages.info(request,f'Hi, You are now logged in as {request.user.username}')
                return redirect('teacher_home',pk=user.id)
            elif user.user_type == '3':
                login(request,user)
                messages.info(request,f'Hi, You are now logged in as {request.user.username}')
                return redirect('student_home',pk=user.id)
        else:
            messages.info(request,"Invalid Username or Password")
            return redirect('loginpage')
    return render(request,'login.html') 


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.info(request,"You are successfully logged out...")
        return redirect('home')
    

def teacherregister(request):
    
    return render(request,'teacher_register.html')
    
def register_teacher(request):
    
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        user_type = request.POST['user_type']
        age = request.POST['age']
        contact = request.POST['mobile']
        pic = request.FILES.get('picture')
        course = request.POST['sel']
       
        if CustomUser.objects.filter(username=username).exists():
            messages.info(request,"Username already taken!!")
            return redirect('teacherregister')
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request,"Email ID already registered!!")
            return redirect('teacherregister')
        if not email.endswith('.com'):
            messages.info(request,"Invalid Email!!")
            return redirect('teacherregister')

        user = CustomUser.objects.create_user(
            first_name=fname,
            last_name=lname,
            email=email,
            username=username,
            user_type=user_type
        )
        user.save()
        teacher = Teacher(
            user=user,
            course=course,
            age=age,
            mobile=contact,
            Image = pic,   
        )
        teacher.save()
        
        messages.info(request,'Registration success! Please wait for admin approval')
        return redirect('teacherregister')
    
def teacher_home(request,pk):

    if request.user.is_authenticated and request.user.user_type == '2':
        user = CustomUser.objects.get(id=pk)
        teacher = Teacher.objects.get(user=user)
        return render(request,'teacher_home.html',{'teacher':teacher})
    else:
        messages.info(request,"Access denied.")
        return redirect('home')
    
def studentregister(request):
    
    return render(request,'student_register.html')
    
def register_student(request):
    
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        user_type = request.POST['user_type']
        age = request.POST['age']
        contact = request.POST['mobile']
        pic = request.FILES.get('picture')
        course = request.POST['sel']
       
        if CustomUser.objects.filter(username=username).exists():
            messages.info(request,"Username already taken!!")
            return redirect('studentregister')
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request,"Email ID already registered!!")
            return redirect('studentregister')
        if not email.endswith('.com'):
            messages.info(request,"Invalid Email!!")
            return redirect('studentregister')

        user = CustomUser.objects.create_user(
            first_name=fname,
            last_name=lname,
            email=email,
            username=username,
            user_type=user_type
        )
        user.save()
        student = Student(
            user=user,
            course=course,
            age=age,
            mobile=contact,
            Image = pic,   
        )
        student.save()
        
        messages.info(request,'Registration success!Please wait for admin approval')
        return redirect('studentregister')
    

def student_home(request,pk):
    
    if request.user.is_authenticated and request.user.user_type == '3':
        user = CustomUser.objects.get(id=pk)
        student = Student.objects.get(user=user)
        return render(request,'student_home.html',{'student':student})
    else:
         messages.info(request,"Access denied.")
         return redirect('home')


def approve(request,pk):

    user = CustomUser.objects.get(id=pk)
    user.status = 1
    user.save()

    password = str(random.randint(100000,999999))
    user.set_password(password)
    user.save()

    send_mail('Admin Approved',
                f'Username : {user.username}\nPassword : {password}\nEmail : {user.email}',
                settings.EMAIL_HOST_USER,[user.email]
                )
    if user.user_type=='2':
        messages.info(request,'Teacher request Approved')
    elif user.user_type=='3':
        messages.info(request,'Student request Approved')
    
    return redirect('userdetails')

def disapprove(request,pk):

    user = CustomUser.objects.get(id=pk)
    email = user.email

    if user.user_type == '2':
        Teacher.objects.filter(user=user).delete()
        messages.info(request,'Teacher request Disapproved')
    elif user.user_type == '3':
        Student.objects.filter(user=user).delete()
        messages.info(request,'Student request Disapproved')

    send_mail('Admin Disapproved',f'Your request has been disapproved by the admin.',settings.EMAIL_HOST_USER,[email])
    user.delete()
    
    return redirect('userdetails')


def resetpage(request):

    return render(request,'reset.html')

def reset(request):

    if request.method == 'POST':

        current = request.POST['current']
        new_pass = request.POST['new']
        confirm_pass = request.POST['confirm']

        user = CustomUser.objects.get(id = request.user.id)
        if not check_password(current,user.password):
            messages.error(request,"Current Password is incorrect!!")
            return redirect('resetpage')
        if new_pass == confirm_pass:
            if len(new_pass)<6 or not any(char.isupper() for char in new_pass) or not any(char.isdigit() for char in new_pass) or not any(char in '!@#$%^&*()_+=[]{}|\;:,.<>?/~' for char in new_pass):
                messages.error(request,"Password must be atleast 6 characters long and contain atleast 1 uppercase, 1 digit and 1 special character")
                return redirect("resetpage")
            else:
                user.password = new_pass
                user.set_password(new_pass)
                user.save()
                messages.info(request,"Password Changed...")
                send_mail('Password changed',
                          f'Username : {user.username}\nNew Password : {new_pass}\nEmail : {user.email}',
                          settings.EMAIL_HOST_USER,[user.email]
                )
                return redirect('loginpage')
        else:
            messages.info(request,"New Password and Confirm Password do not match..")
            return redirect('resetpage')