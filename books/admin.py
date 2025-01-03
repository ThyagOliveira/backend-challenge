from django.contrib import admin
from .models import Book, Reservation


class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status')


admin.site.register(Book, BooksAdmin)
admin.site.register(Reservation, ReservationAdmin)