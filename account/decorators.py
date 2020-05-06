#reference https://stackoverflow.com/questions/5678585/django-tweaking-login-required-decorator

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Account

def teacher_student_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        teacher_or_student = Account.objects.filter(pk=request.user.id, groups__name='Teacher/Student').exists()
        if not teacher_or_student:  # if not coach redirect to home page
            return HttpResponseRedirect(reverse('home'))
        else:
            return function(request, *args, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


def guest_or_teacher_student_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        if 'guest' in request.session:
            return function(request, *args, **kwargs)
        teacher_or_student = Account.objects.filter(pk=request.user.id, groups__name='Teacher/Student').exists()
        if not teacher_or_student:  # if not coach redirect to home page
            return HttpResponseRedirect(reverse('home'))
        else:
            return function(request, *args, **kwargs)
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


def loggedout(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        teacher_or_student = Account.objects.filter(pk=request.user.id, groups__name='Teacher/Student').exists()
        if not teacher_or_student and 'guest' not in request.session:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home', args=(), kwargs={}))

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper




