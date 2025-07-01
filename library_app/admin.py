from django.contrib import admin
from .models import User, LibraryContactInfo, Library, Book, Genre

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(LibraryContactInfo)
admin.site.register(User)


