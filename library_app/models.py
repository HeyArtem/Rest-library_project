from django.db import models
from django.contrib.auth.models import AbstractUser


class Library(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "libraries"
        verbose_name = "Библиотека"
        verbose_name_plural = "Библиотеки"


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="users/avatar/", null=True, blank=True, verbose_name="Аватар"
    )
    library = models.ManyToManyField(Library, related_name='users')

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class LibraryContactInfo(models.Model):
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True, related_name='info')
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.library}-{self.phone}"

    class Meta:
        db_table = "libraryContactInfo"
        verbose_name = "Информация о библиотеке"
        verbose_name_plural = "Информация о библиотеке"


class Genre(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "genres"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    year_of_release = models.PositiveIntegerField()
    picture = models.ImageField(upload_to='book_pictures/', null=True, blank=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='genres')

    def __str__(self):
        return f"{self.title}-{self.genre}"

    class Meta:
        db_table = "books"
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
