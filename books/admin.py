from django.contrib import admin
from .models import Book


class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors')


admin.site.register(Book, BooksAdmin)
