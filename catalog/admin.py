from django.contrib import admin

# Register your models here.

from .models import *

class BookInline(admin.TabularInline):
    model = Book
	
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    fields = ['first_name', 'last_name']
    inlines = [BookInline]

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    #inlines = [BookInstanceInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher)
admin.site.register(BookReservation)
admin.site.register(BookReview)