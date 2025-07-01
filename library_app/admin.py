from django.contrib import admin

from .models import Book, Genre, Library, LibraryContactInfo, User

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(LibraryContactInfo)
admin.site.register(User)
