from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import *
from account.models import Account
from account.decorators import login_required, teacher_student_required, guest_or_teacher_student_required, loggedout
# Create your views here.

def home(request):
    if Account.objects.filter(pk=request.user.id, groups__name='Teacher/Student').exists() or 'guest' in request.session:
        return HttpResponseRedirect(reverse('books'))
    elif Account.objects.filter(pk=request.user.id, groups__name='Book Manager').exists():
        return HttpResponseRedirect(reverse('bookmanager'))
    else: 
        return HttpResponseRedirect(reverse('signin'))

@guest_or_teacher_student_required
def books(request):
    book = Book.objects.all()
    return render(request, 'catalogv2/books.html', {'book': book})

@guest_or_teacher_student_required
def book_instance(request, pk):
    if request.method == 'POST':
        reserveBook(request, pk)

    book = Book.objects.get(id=pk)
    instance = BookInstance.objects.filter(book=pk)
    review = BookReview.objects.filter(book=pk)
    context = {'book':book, 'instance':instance, 'user': request.user, 'review': review}
    return render(request, 'catalogv2/book_instance.html', context)

@teacher_student_required
def reserveBook(request, pk):
    instance_id = request.POST.get('instance_id')
    reserve = BookInstance.objects.get(id=str(instance_id))
    reserve.due_back = default_due()
    reserve.status = 'r'
    reserve.save()
    reservation = BookReservation.objects.create(user=request.user, book_instance = reserve)
    reservation.save()

@teacher_student_required
def profile(request):
    borrowed_book = BookReservation.objects.filter(user=request.user)
    review = BookReview.objects.filter(user=request.user)
    return render(request, 'catalogv2/profile.html', {'borrowed_book': borrowed_book, 'review': review})

def returnBook(request, pk):
    instance_id = request.POST.get('instance_id')
    instance = BookInstance.objects.get(id=str(instance_id))
    instance.status = 'a'
    instance.save()
    reservation = BookReservation.objects.filter(book_instance = instance)
    reservation.date_return = timezone.now()
    reservation.save()

@teacher_student_required
def reviewBook(request, pk):
    book= Book.objects.get(id=pk)
    book_review = BookReview.objects.create(user=request.user, text = request.POST.get('review'), book = book)
    book_review.save()
    review = BookReview.objects.filter(book=book)

@guest_or_teacher_student_required
def review(request, pk):
    if request.method == 'POST':
        reviewBook(request, pk)
    
    book= Book.objects.get(id=pk)
    review = BookReview.objects.filter(book=book)
    return render(request, "catalogv2/bookreview.html", {'review': review, 'book': book, "id": book.id})

@guest_or_teacher_student_required
def search(request):
    q = request.GET.get('search')
    book = Book.objects.filter(title__contains=q)
    return render(request, "catalogv2/booksearch.html", {'search': q, 'book': book})

#reference https://stackoverflow.com/questions/37688730/django-ajax-search-function
#reference https://simpleisbetterthancomplex.com/tutorial/2016/07/27/how-to-return-json-encoded-response.html
#search suggestion
@guest_or_teacher_student_required
def suggest(request):
    book= Book.objects.all().values()
    return JsonResponse({'data': list(book)})

