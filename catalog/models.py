from django.db import models
from account.models import Account
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Publisher(models.Model):
	publisher = models.CharField(max_length=200, help_text='Enter Book\'s Publisher')

	def __str__(self):
		return self.publisher

from django.urls import reverse
	
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null = True)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN Number')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, blank = True)
    yearPub = models.DateField(null=True)
	
    def __str__(self):
        return self.title

class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	
	class Meta:
		ordering = ['last_name', 'first_name']
		
	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

import uuid

class BookInstance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
	book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	due_back = models.DateField(null=True, blank=True,  editable=True)
	
	LOAN_STATUS = (('a', 'Available'),
		('r', 'Reserved'),)
	
	status = models.CharField(max_length=1,
		choices= LOAN_STATUS,
		blank = True,
		default = 'm',
		help_text = 'Book Availability',)
	
		
	def __str__(self):
		return f'{self.id} ({self.book.title})'

def default_due():
   return timezone.now() + timezone.timedelta(days=30)

class BookReservation(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	book_instance = models.ForeignKey(BookInstance, on_delete=models.SET_NULL, null = True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	date_reservation = models.DateField(verbose_name="Date borrowed: ", editable=False, auto_now_add=True)
	class Meta:
		ordering = ['-date_reservation']

	def __str__(self):
		return f'{self.id}'

class BookReview(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.SET_NULL, null = True)
	text = models.TextField(max_length=1000)



