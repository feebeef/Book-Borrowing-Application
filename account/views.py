# Create your views here.
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .decorators import login_required, teacher_student_required, guest_or_teacher_student_required, loggedout
from django.contrib.auth.models import Group
from .models import Account

@login_required
def logout_user(request):
    logout(request)
    return render(request, 'auth/signin.html', {})

@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, "auth/settings.html")

    if request.POST.get('new') != request.POST.get('conf'):
        return render(request, 'auth/settings.html', {'error': 'password did not match', 'validate': 'invalid'})
    elif request.user.password != request.POST.get('old'):
        return render(request, 'auth/settings.html', {'error': 'invalid old password', 'validate': 'invalid'})
    else:
        request.user.set_password(request.POST(new))
        return HttpResponseRedirect(reverse('home'))
    
def init_form(data, username_err,  password_err, email_err, idnum_err):
    new_user_form = UserForm(data=data, username_err = username_err, password_err = password_err,
                             email_err = email_err, idnum_err = idnum_err)
    return new_user_form

def register(request):
    if request.method == 'GET':
        user_form = init_form({}, False, False,False, False)
        return render(request,'auth/register.html', {'form': user_form})
    
    form = init_form(request.POST, False, False,False, False)
    if form.is_valid():
        user = form.save()
        user.set_password(user.password, )
        user.groups.add(Group.objects.get(name='Teacher/Student'))
        user.save()
        if 'guest' in request.session:
            request.session.flush()
        return HttpResponseRedirect(reverse('signin'))
    else:
        invalid_form = init_form(request.POST, 
                                form.has_error('username',code=None),
                                form.has_error('password', code=None),
                                form.has_error('email',code=None),
                                form.has_error('idnumm',code=None))
        return render(request,'auth/register.html', {'form':invalid_form})

@loggedout
def signin(request):
    if request.method == 'GET':
         return render(request, 'auth/signin.html', {})
    elif request.POST.get('guest'):
        return signin_as_guest(request)
    elif (user := authenticate(username=request.POST.get('username'), password=request.POST.get('password')) ) and user.is_active:
            login(request,user)
            return HttpResponseRedirect(reverse('books'))
    else:
        return render(request, 'auth/signin.html', {'error': 'Invalid username or password', 'validate': 'invalid'})
                
def signin_as_guest(request):
    request.session['guest'] = True
    request.session['username'] = 'guest'
    request.session.save()
    return HttpResponseRedirect(reverse('home'))