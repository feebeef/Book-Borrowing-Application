# Create your views here.
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .decorators import login_required, teacher_student_required, guest_or_teacher_student_required, loggedout
from django.contrib.auth.models import Group
from .models import Account

@guest_or_teacher_student_required
def logout(request):
    logout(request.user)
    return HttpResponseRedirect(reverse('home'))

@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, "auth/settings.html")

    if request.POST.get('new') != request.POST.get('conf'):
        return render(request, 'auth/settings.html', {'error': 'password does not match', 'validate': 'invalid'})
    elif request.user.password != request.POST.get('old'):
        return render(request, 'auth/settings.html', {'error': 'invalid old password', 'validate': 'invalid'})
    else:
        request.user.set_password()
        return HttpResponseRedirect(reverse('home'))
    
def init_form(data, username_err,  password_err, email_err, idnum_err):
    new_user_form = UserForm(data=data, username_err = username_err, password_err = password_err,
                             email_err = email_err, idnum_err = idnum_err)
    return new_user_form

def register(request):
    if request.method == 'GET':
        user_form = init_form({}, False, False,False, False)
        return render(request,'auth/register.html', {'form': user_form})

    if  (form := UserForm(data=request.POST)).is_valid():
        user = form.save()
        user.set_password(user.password)
        user.groups.add(Group.objects.get(name='Teacher/Student'))
        user.save()
        request.session.flush()
        return HttpResponseRedirect(reverse('signin'))
    else:
        invalid_form = init_form(request.POST, 
                        user_form.has_error('username',code=None),
                        user_form.has_error('password', code=None),
                        user_form.has_error('email',code=None),
                        user_form.has_error('idnumm',code=None))
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