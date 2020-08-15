from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from djangotestproject.settings import EMAIL_HOST_USER
from .models import Users, Subscribers

# Create your views here.

def firstPageController(request):
    return  HttpResponse("<h1> heyy</h1>")

def IndexPageController(request):
    return  HttpResponseRedirect('/homePage')

def HtmlPageController(request):
    return  render(request, 'htmlpage.html')

def HtmlPageControllerWithData(request):
    data1 = 'This is data 1 passing to html page'
    data2 = 'This is data 2 passing to html page'
    return  render(request, 'htmlpage_with_data.html', {'data': data1, 'data1': data2 })

def PassingDataController(request, url_data):
    return HttpResponse('<h2> this is data coming via url: '+ url_data)

@login_required(login_url='/login_user/')
def addData(request):
    return render(request, 'add_data.html')


@login_required(login_url='/login_user/')
def add_users(request):
    if request.method!='POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        try:
            user = Users(name=request.POST.get('name', ''), email=request.POST.get('email',''), )
            user.save()
            messages.success(request, "Added Successfully")
        except:
            messages.error(request, "Failed to Add User")

        return HttpResponseRedirect('/addData')


@login_required(login_url='/login_user/')
def add_subscribers(request):
    if request.method!='POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        try:
            subscriber = Subscribers(name=request.POST.get('name', ''), email=request.POST.get('email',''), )
            subscriber.save()
            messages.success(request, "Added Successfully")
        except:
            messages.error(request, "Failed to Add Subscriber")

        return HttpResponseRedirect('/addData')


@login_required(login_url='/login_user/')
def show_all_data(request):
    all_users=Users.objects.all()
    all_subscribers=Subscribers.objects.all()
    users = []
    subscribers = []
    for i in range(0, len(all_users), 1):
        users.append({"id": all_users[i].id, "name": all_users[i].name, "email":  all_users[i].email, "created_at": all_users[i].created_at})
    print(users)
    for i in range(0, len(all_subscribers), 1):
        subscribers.append({"id": all_subscribers[i].id, "name": all_subscribers[i].name, "email":  all_subscribers[i].email, "created_at": all_subscribers[i].created_at})
    return render(request, 'show_data.html', {'users': users, 'subscribers': subscribers})


@login_required(login_url='/login_user/')
def update_user(request, user_id):
    user = Users.objects.get(id=user_id)
    print(user)
    if user==None:
        return HttpResponse('User Not Found')
    else:
        return render(request, 'user_edit.html', {'user':user})


@login_required(login_url='/login_user/')
def delete_user(request, user_id):
    user=Users.objects.get(id=user_id)
    user.delete()

    messages.error(request, 'Deleted Successfully')
    return HttpResponseRedirect('/show_all_data')


@login_required(login_url='/login_user/')
def edit_user(request):
    if request.method!='POST':
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        user=Users.objects.get(id=request.POST.get('id', ''))
        if user==None:
            return HttpResponse('<h2>User Not Found</h2>')
        else:
            user.name=request.POST.get('name', '')
            user.email=request.POST.get('email', '')
            user.save()

            messages.success(request, 'Updated Successfully')
            return HttpResponseRedirect('update_user/'+str(user.id)+'')


@login_required(login_url='/login_user/')
def update_subscriber(request, subscriber_id):
    subscriber = Subscribers.objects.get(id=subscriber_id)
    print(subscriber)
    if subscriber==None:
        return HttpResponse('Subscriber Not Found')
    else:
        return render(request, 'subscriber_edit.html', {'subscriber':subscriber})


@login_required(login_url='/login_user/')
def delete_subscriber(request, subscriber_id):
    subscriber=Subscribers.objects.get(id=subscriber_id)
    subscriber.delete()

    messages.error(request, 'Deleted Successfully')
    return HttpResponseRedirect('/show_all_data')


@login_required(login_url='/login_user/')
def edit_subscriber(request):
    if request.method!='POST':
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        subscriber=Subscribers.objects.get(id=request.POST.get('id', ''))
        if subscriber==None:
            return HttpResponse('<h2>Subscriber Not Found</h2>')
        else:
            subscriber.name=request.POST.get('name', '')
            subscriber.email=request.POST.get('email', '')
            subscriber.save()

            messages.success(request, 'Updated Successfully')
            return HttpResponseRedirect('update_subscriber/'+str(subscriber.id)+'')




def LoginUser(request):
    if request.user == None or  request.user == '' or request.user.username == '':
        return render(request, 'login_page.html')
    else:
        return HttpResponseRedirect('/homePage')


def RegisterUser(request):
    if request.user == None:
        return render(request, 'register_page.html')
    else:
        return HttpResponseRedirect('/homePage')

def SaveUser(request):
    if request.method!='POST':
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        username=request.POST.get('username', '')
        email=request.POST.get('email', '')
        password=request.POST.get('password', '')

        if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            User.objects.create_user(username,email,password)
            messages.success(request, 'User Created Successfully')
            return HttpResponseRedirect('/register_user')
        else:
            messages.error(request, 'Username or Email ALready Exists')
            return HttpResponseRedirect('/register_user')


def DoLoginUser(request):
    if request.method!='POST':
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        username=request.POST.get('username', '')
        password=request.POST.get('password', '')
        user=authenticate(username=username, password=password)
        login(request,user)

        if user!=None:
            return HttpResponseRedirect('/homePage')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return HttpResponseRedirect('/login_user')

@login_required(login_url='/login_user/')
def HomePage(request):
    return render(request, 'home_page.html')

def LogoutUser(request):
    logout(request)
    request.user=None
    return HttpResponseRedirect('/login_user')

def SendPlainMail(request):
    message=request.POST.get('message', '')
    subject=request.POST.get('subject', '')
    mail_id=request.POST.get('email', '')
    recipient_list = ['preetiwali212@gmail.com', 'test@gmail.com', 'preetitest2@gmail.com']
    email=EmailMessage(subject, message, EMAIL_HOST_USER,[mail_id, recipient_list])
    email.content_subtype='html'
    email.send()
    return HttpResponse('Sent')

def send_mail_plain_with_file(request):
    message=request.POST.get('message', '')
    subject=request.POST.get('subject', '')
    mail_id=request.POST.get('email', '')
    email=EmailMessage(subject, message, EMAIL_HOST_USER,[mail_id])
    email.content_subtype='html'

    file=request.FILES['file']
    email.attach(file.name, file.read(), file.content_type)
    email.send()
    return HttpResponse('Sent')

def setSession(request):
    request.session['session_data_1']='This is session 1 data'
    request.session['session_data_2']='This is session 2 data'
    return HttpResponse('Session Set')

def view_session(request):
    if request.session.has_key('session_data_1'):
        session_data_1=request.session['session_data_1']
    else:
        session_data_1='Data is Blank'

    if request.session.has_key('session_data_2'):
        session_data_2=request.session['session_data_2']
    else:
        session_data_2='Data is Blank'

    return render(request, 'show_session_data.html', {'session_data_1': session_data_1, 'session_data_2': session_data_2})

def del_session(request):
    del request.session['session_data_1']
    del request.session['session_data_2']
    return HttpResponse('Session Deleted')