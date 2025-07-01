План:
модель library
	title
	address
	user (`ManyToMany` c user)
	books

модель user
	name
	email
	birthday

модель book
	id (`ForeignKey` c library)
	title
	description
	picture
	genre
	year_of_release

модель genre
	title (`ForeignKey` c book)
	description

Проверь, нормально и хочется еще One to one добавить


% mkdir library_project
% cd library_project
% python3 -m venv venv
% source venv/bin/activate
% pip install -U pip && pip install -U setuptools
% brew update # Обновляет информацию о доступных пакетах
% brew upgrade	# Обновляет установленные пакеты
% brew cleanup	# Удаляет старые версии пакетов
% pip install django==4.2.1
% pip install djangorestframework
% python -m pip install Pillow
% django-admin startproject library_project .  ( 💠Точка (.) в конце говорит Django, что не надо создавать лишнюю вложенную папку!)
python manage.py startapp library_app
python manage.py runserver

library_project/settings.py

	import os
	from pathlib import Path

	# Build paths inside the project like this: BASE_DIR / 'subdir'.
	BASE_DIR = Path(__file__).resolve().parent.parent


	# Quick-start development settings - unsuitable for production
	# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

	# SECURITY WARNING: keep the secret key used in production secret!
	SECRET_KEY = 'django-insecure-zvaj#_43%q29*!w=)2+c=)6&jb!#b#nn8t)k-%solzuv@3waqa'

	# SECURITY WARNING: don't run with debug turned on in production!
	DEBUG = True

	ALLOWED_HOSTS = []


	# Application definition

	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'rest_framework',
	    'library_app',
	]

	MIDDLEWARE = [
	    'django.middleware.security.SecurityMiddleware',
	    'django.contrib.sessions.middleware.SessionMiddleware',
	    'django.middleware.common.CommonMiddleware',
	    'django.middleware.csrf.CsrfViewMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	    'django.contrib.messages.middleware.MessageMiddleware',
	    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	]

	ROOT_URLCONF = 'library_project.urls'

	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [],
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                'django.template.context_processors.debug',
	                'django.template.context_processors.request',
	                'django.contrib.auth.context_processors.auth',
	                'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]

	WSGI_APPLICATION = 'library_project.wsgi.application'


	# Database
	# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': BASE_DIR / 'db.sqlite3',
	    }
	}


	# Password validation
	# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

	AUTH_PASSWORD_VALIDATORS = [
	    {
	        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	    },
	    {
	        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	    },
	    {
	        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	    },
	    {
	        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	    },
	]


	# Internationalization
	# https://docs.djangoproject.com/en/4.2/topics/i18n/

	LANGUAGE_CODE = 'Europe/Moscow'

	TIME_ZONE = 'UTC'

	USE_I18N = True

	USE_TZ = True


	STATIC_URL = 'static/'
	STATIC_ROOT = os.path.join(BASE_DIR, "static")

	MEDIA_URL = "media/"
	MEDIA_ROOT = os.path.join(BASE_DIR, "media")

	# Вместо стандартной модели пользователя (auth.User) используй мою собственную модель User из приложения library_app
	AUTH_USER_MODEL = "library_app.User"

	DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



	* * * * Показать структуру проекта в графическом виде: * * * *

	brew install tree  # для macOS 	# Если tree не установлен, сначала установи его:
	tree	# вывести дерево папок:
	tree -L 2	# показать только 2-3 уровня вложенности:
	tree > structure.txt
	* * * * * * * * * * * * * * * *


		.
	├── db.sqlite3
	├── library_app
	│   ├── __init__.py
	│   ├── __pycache__
	│   ├── admin.py
	│   ├── apps.py
	│   ├── migrations
	│   ├── models.py
	│   ├── tests.py
	│   └── views.py
	├── library_project
	│   ├── __init__.py
	│   ├── __pycache__
	│   ├── asgi.py
	│   ├── settings.py
	│   ├── urls.py
	│   └── wsgi.py
	├── manage.py
	├── notes
	│   └── notes_library_app.py
	└── venv
	    ├── bin
	    ├── include
	    ├── lib
	    └── pyvenv.cfg


library_app/models.py
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


python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

	Username (leave blank to use 'heyartem'):art
		Email address:
		Password: 0000
		Password (again): 0000


❗️-Настраиваю debuger
        Current File-Edit Configuration-+-Python-Name('Debuger')-Script path(путь до manage.py)-
                Parameters(runserver)-Apply OK
✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅

Я хочу уметь писать разные способы представлений
+-----------------------------+----------------------------------------+----------------------------------------+
|        Тип представления    |                Плюсы                   |                Минусы                  |
+-----------------------------+----------------------------------------+----------------------------------------+
| 1. APIView                  | - Полный контроль над логикой         | - Много кода                           |
|                             | - Гибкость                            | - Нужно писать всё вручную              |
+-----------------------------+----------------------------------------+----------------------------------------+
| 2. GenericAPIView           | - Быстро создаются CRUD               | - Меньше гибкости                      |
| (ListCreateAPIView,         | - Подходят для большинства случаев     | - Не всегда подходит для кастомных задач|
| RetrieveUpdateDestroyAPIView)|                                        |                                        |
+-----------------------------+----------------------------------------+----------------------------------------+
| 3. ViewSet + Router         | - Все CRUD в одном классе              | - Может быть сложно при тонкой настройке|
| (ModelViewSet)             | - Автоматическая маршрутизация URL     | - Неочевидно для новичков              |
+-----------------------------+----------------------------------------+----------------------------------------+
| 4. Функциональные view      | - Простота                            | - Неудобно масштабировать               |
| с @api_view                 | - Хорошо подходит для прототипирования| - Нет автоматической маршрутизации      |
+-----------------------------+----------------------------------------+----------------------------------------+


✅ Представление на основе ViewSet

	library_app/views.py
		from rest_framework import viewsets
		from .models import Book
		from .serializers import BookSerializer

		class BookViewSet(viewsets.ModelViewSet):
		    """
		        ViewSet для модели Book. Обеспечивает стандартные операции:
		        - GET /books/ (список)
		        - POST /books/
		        - GET /books/{id}/ (детали)
		        - PUT /books/{id}/
		        - DELETE /books/{id}/
		    """
		    queryset = Book.objects.all().order_by('-id')
		    serializer_class = BookSerializer



	library_app/serializers.py
		from rest_framework import serializers
		from rest_framework.serializers import Serializer

		from .models import Book
		from datetime import datetime

		class BookSerializer(serializers.ModelSerializer):
		    class Meta:
		        model =Book
		        fields = (
		        	"id",
		            "title",
		            "description",
		            "year_of_release",
		            "picture",
		            "library",
		            "genre",

		        )
		    def validate_year_of_release(self, year):
		        """
		        Валидатор года.
		        Этот метод автоматически вызывается при вызове: serializer.is_valid()
		        """
		        current_year = datetime.now().year
		        if year < 1000 or year > current_year:
		            raise serializers.ValidationError(
		                f"Год должен быть между 1000 и {current_year} "
		            )
		        return year



	library_project/urls.py
		from django.contrib import admin
		from django.urls import path, include

		urlpatterns = [
		    path('admin/', admin.site.urls),
		    path('api/', include('library_app.urls')),
		]




	library_app/urls.py
		from django.urls import include, path
		from rest_framework.routers import DefaultRouter
		from .views import BookViewSet
		from library_project import settings
		from django.conf.urls.static import static

		router = DefaultRouter()
		router.register(r'books', BookViewSet, basename='book')
		# basename='book' нужен, если DRF не может сам определить имя маршрута (например, если ты не указал queryset в ViewSet


		urlpatterns = [
		    path('', include(router.urls) ),
		]
		if settings.DEBUG:
		    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

		'''
		Роутер автоматически создаёт все нужные маршруты:

		GET /books/
		POST /books/
		GET /books/1/
		PUT /books/1/
		DELETE /books/1/

		http://localhost:8000/books/
		    Ты увидишь интерфейс DRF с возможностью:

		    Просмотреть список книг
		    Добавить новую книгу
		    Редактировать и удалять книги
		'''

	test
	http://127.0.0.1:8000/api/books/
	все книги
	Валидация не работает через админку, так задумано

	post
		POST http://127.0.0.1:8000/api/books/
		(Body, form-data, в поле picture-> file)

	get
		http://127.0.0.1:8000/api/books/5/

	delete
		http://127.0.0.1:8000/api/books/11/

	patch
		http://127.0.0.1:8000/api/books/13/


	🧩 Я хочу добавить @action.
		🎲 Это декоратор для ViewSet, который позволяет:
			Добавлять дополнительные эндпоинты к твоим ресурсам.
			Не использовать отдельные URL и представления для каждой мелкой операции.
			Сгруппировать логику внутри одного ViewSet.

		Вместо того чтобы создавать отдельное представление:
			# urls.py
			path('books/latest/', views.LatestBookView.as_view())

		Ты можешь добавить действие прямо в ViewSet :
			# views.py
			class BookViewSet(viewsets.ModelViewSet):
			    ...

			    @action(detail=False, methods=['get'])
			    def latest(self, request):
			        ...
		И получить:
			GET /books/latest/

		📌 Как называется?
			Называется: @action
			Относится к классу: rest_framework.decorators.action
			Используется только в ViewSet (например, ModelViewSet, GenericViewSet)

		📌 Для чего используется?
		Чтобы добавить кастомные действия к ресурсу, например:
			/books/latest/ 		  Получить последние книги
			/books/5/like/ 		  Поставить "лайк" книге
			/books/statistics/	  	Получить статистику по книгам
			/books/import/	  Импортировать книги из файла

		📌 Объяснение параметров:
			@action(detail=???, methods=[???], url_path=???)

			detail	True	— действие относится к одному объекту<br>
					False	— ко всей коллекции

					detail=True → /books/5/like/
					detail=False → /books/latest/

			methods	Список HTTP-методов['get'],['post'],['patch', 'put']

			url_path Путь в URL (можно изменить на любой)
			url_path='top' → /books/top/
			url_name	Необязательный параметр для именования маршрута Редко используется

Получить 5 последних книг на @action
library_app/views.py
	from django.core.serializers import serialize
	from rest_framework import viewsets, status
	from rest_framework.response import Response

	from .models import Book
	from .serializers import BookSerializer
	from rest_framework.decorators import action

	class BookViewSet(viewsets.ModelViewSet):
	    """
	        ViewSet для модели Book. Обеспечивает стандартные операции:
	        - GET /books/ (список)
	        - POST /books/
	        - GET /books/{id}/ (детали)
	        - PUT /books/{id}/
	        - DELETE /books/{id}/
	    """
	    queryset = Book.objects.all().order_by('-id')
	    serializer_class = BookSerializer

	    @action(detail=False, methods=['get'], url_path='latest')
	    def latest_books(self, request):
	        """
	       Возвращает последние 5 книг
	       GET /books/latest/
	       """
	        books = Book.objects.order_by('-year_of_release')[:5]
	        serializer = self.get_serializer(books, many=True)
	        return Response(serializer.data, status=status.HTTP_200_OK)


	test postman
		get
			http://127.0.0.1:8000/api/books/latest/

	просто пример использования @action + POST
	(я не использую, у меня нет поля с лайками)
		from rest_framework import viewsets, status
		from rest_framework.decorators import action
		from rest_framework.response import Response

		from .models import Book
		from .serializers import BookSerializer

		class BookViewSet(viewsets.ModelViewSet):
		    queryset = Book.objects.all()
		    serializer_class = BookSerializer

		    @action(detail=True, methods=['post'], url_path='like')
		    def like_book(self, request, pk=None):
		        """
		        Добавляет лайк книге
		        POST /books/1/like/
		        """
		        book = self.get_object()
		        book.likes += 1
		        book.save()
		        return Response({'status': 'liked', 'total_likes': book.likes}, status=status.HTTP_200_OK)



✅ Представление на основе APIView (полный контроль!)
	library_app/serializers.py
		сериалайзер уже есть


		from rest_framework import viewsets, status
		from rest_framework.response import Response

		from .models import Book
		from .serializers import BookSerializer
		from rest_framework.decorators import action
		from rest_framework.views import APIView
		from django.shortcuts import get_object_or_404


		class BookViewSet(viewsets.ModelViewSet):
		    """
		        ViewSet для модели Book. Обеспечивает стандартные операции:
		        - GET /books/ (список)
		        - POST /books/
		        - GET /books/{id}/ (детали)
		        - PUT /books/{id}/
		        - DELETE /books/{id}/
		        - PATCH
		    """
		    queryset = Book.objects.all().order_by('-id')
		    serializer_class = BookSerializer

		    @action(detail=False, methods=['get'], url_path='latest')
		    def latest_books(self, request):
		        """
		       Возвращает последние 5 книг
		       GET /books/latest/
		       """
		        books = Book.objects.order_by('-year_of_release')[:5]
		        serializer = self.get_serializer(books, many=True)
		        return Response(serializer.data, status=status.HTTP_200_OK)


		class BookListCreateAPIView(APIView):
		    """
		    Второй способ реализации-APIView
		    Вывод всех книг, поиск по title, создание книги
		    """

		    def get(self, request, *args, **kwargs):
		        books = Book.objects.order_by('-id')
		        search = request.query_params.get('search')
		        if search:
		            print('[!] search:', search)
		            books = books.filter(title__icontains=search)

		        return Response(
		            BookSerializer(books, many=True).data, status=status.HTTP_200_OK
		        )

		    def post(self, request):
		        serializer = BookSerializer(data=request.data)

		        if serializer.is_valid():
		            serializer.save()
		            return Response(serializer.data, status=status.HTTP_201_CREATED)
		        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		class BookDetailAPIView(APIView):
		    """
		    Второй способ реализации-APIView
		    POST, GET (/books/{id}/), PUT, PATCH, DELETE

		    """

		    def get_object(self, pk):
		        """
		        Вспомогательный метод: пытается найти книгу по ID (pk)
		        Если не найдена — возвращает None
		        """
		        return get_object_or_404(Book, pk=pk)

		        # try:
		        #     return Book.objects.get(pk=pk)
		        # except Book.DoesNotExist:
		        #     return None

		    def get(self, request, pk):
		        """
		        GET /api/Abooks/{id}/
		        Возвращает данные о конкретной книге по id
		        """
		        book = self.get_object(pk)
		        if not book:
		            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
		        serializer = BookSerializer(book).data
		        return Response(serializer, status=status.HTTP_200_OK)

		    def delete(self, request, pk):
		        """
		        DELETE /api/Abooks/{id}/
		        Удаляет книгу
		        """
		        book = self.get_object(pk)
		        if not book:
		            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
		        book.delete()
		        return Response(status=status.HTTP_204_NO_CONTENT)

		    def put(self, request, pk):
		        """
		        PUT /api/Abooks/{id}/
		        Полное обновление данных книги
		        """
		        book = self.get_object(pk)
		        if not book:
		            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
		        serializer = BookSerializer(book, data=request.data)
		        if serializer.is_valid():
		            serializer.save()
		            return Response(serializer.data, status=status.HTTP_200_OK)
		        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		    def patch(self, request, pk):
		        """
		        PATCH /api/Abooks/{id}/
		        Частичное обновление (можно обновить только одно поле)
		        """
		        book = self.get_object(pk)
		        if not book:
		            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
		        serializer = BookSerializer(book, data=request.data, partial=True)  # Частичное обновление
		        if serializer.is_valid():
		            serializer.save()
		            return Response(serializer.data, status=status.HTTP_200_OK)
		        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



	library_app/urls.py
		from django.urls import include, path
		from rest_framework.routers import DefaultRouter
		from .views import BookViewSet, BookListCreateAPIView, BookDetailAPIView
		from library_project import settings
		from django.conf.urls.static import static

		router = DefaultRouter()
		router.register(r'books', BookViewSet, basename='book')
		# basename='book' нужен, если DRF не может сам определить имя маршрута (например, если ты не указал queryset в ViewSet


		urlpatterns = [
		    path('', include(router.urls) ),

		    # Проект на APIView
		    path('Abooks/', BookListCreateAPIView.as_view(), name='book-list'),
		    path('Abooks/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
		]

		if settings.DEBUG:
		    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

		'''
		✅ Роутер автоматически создаёт все нужные маршруты:

		GET /books/
		POST /books/
		GET /books/1/
		PUT /books/1/
		DELETE /books/1/

		http://localhost:8000/books/
		    Ты увидишь интерфейс DRF с возможностью:

		    Просмотреть список книг
		    Добавить новую книгу
		    Редактировать и удалять книги
		'''
	test Postman
		get http://127.0.0.1:8000/api/Abooks/?search=Убийство
		get http://127.0.0.1:8000/api/Abooks/3/
		post http://127.0.0.1:8000/api/Abooks/	(body form-data)
		del http://127.0.0.1:8000/api/Abooks/20/
		put http://127.0.0.1:8000/api/Abooks/17/
		patch http://127.0.0.1:8000/api/Abooks/17/


✅ Представление на Дженериках (Generic Views)
Это готовые классы от DRF, которые предоставляют стандартные действия:
	(ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView 1-й вид Дженериков)

	+-----------------------------+---------------------------------------+
	|         Действие            |             Generic                 |
	+-----------------------------+---------------------------------------+
	| Получить список (GET)       | ListAPIView                         |	http://127.0.0.1:8000/api/Gbooks/
	| Создать объект (POST)       | CreateAPIView                       |	http://127.0.0.1:8000/api/Gbooks/ (Body form-data)
	| Получить один объект (GET) | RetrieveAPIView                      |	http://127.0.0.1:8000/api/Gbooks/18/
	| Обновить объект (PUT)      | UpdateAPIView                        |	http://127.0.0.1:8000/api/Gbooks/18/ (Body form-data)
	| Частично обновить (PATCH)  | UpdateAPIView + partial=True         |	http://127.0.0.1:8000/api/Gbooks/18/ (Body form-data, только обновляемое поле)
	| Удалить объект (DELETE)    | DestroyAPIView                       |	http://127.0.0.1:8000/api/Gbooks/18/
	+-----------------------------+---------------------------------------+

	library_app/views.py
		...
		class BookListCreateGenericView(ListAPIView, CreateAPIView):
		    queryset = Book.objects.all().order_by('-id')
		    serializer_class = BookSerializer

		    """
		    ❓ Можно ли удалить методы get() и post()?
		    да, можно!
		    Потому что:
		        ListAPIView уже имеет метод get(), который вызывает self.list(...)
		        CreateAPIView уже имеет метод post(), который вызывает self.create(...)
		    """
		    # def get(self, request, *args, **kwargs):
		    #     return self.list(request, *args, **kwargs)
		    #
		    # def post(self, request, *args, **kwargs):
		    #     return self.create(request, *args, **kwargs)


		class BookDetailUpdateDeleteView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
		    queryset = Book.objects.all()
		    serializer_class = BookSerializer

		    # def get(self, request, *args, **kwargs):
		    #     return self.retrieve(request, *args, **kwargs)
		    #
		    # def put(self, request, *args, **kwargs):
		    #     return self.update(request, *args, **kwargs)

		    # def patch(self, request, *args, **kwargs):
		    #     return self.partial_update(request, *args, **kwargs)  # partial=True по умолчанию

		    # def delete(self, request, *args, **kwargs):
		    #     return self.destroy(request, *args, **kwargs)
		...

	library_app/urls.py
		...
		urlpatterns = [
		    path('', include(router.urls) ),

		    # Проект на APIView
		    path('Abooks/', BookListCreateAPIView.as_view(), name='book-list'),
		    path('Abooks/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),

		    # Представление на Дженериках ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
		    path('Gbooks/', BookListCreateGenericView.as_view(), name='book-list'),
		    path('Gbooks/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-list'),
		]

		if settings.DEBUG:
		    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
		...

✅ Представление на Дженериках (Generic Views) 2-й вид
	(2-й вид Дженериков: ListCreateAPIView, RetrieveUpdateDestroyAPIView)

	library_app/views.py
		class BookListCreateGenericView2(ListCreateAPIView):
		    queryset = Book.objects.all().order_by('-id')
		    serializer_class = BookSerializer

		class BookDetailUpdateDestroyView2(RetrieveUpdateDestroyAPIView):
		    queryset = Book.objects.all()
		    serializer_class = BookSerializer

	library_app/urls.py
		...
		urlpatterns = [
		    path('', include(router.urls) ),

		    # Проект на APIView
		    path('Abooks/', BookListCreateAPIView.as_view(), name='book-list'),
		    path('Abooks/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),

		    # Представление на Дженериках ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
		    path('Gbooks/', BookListCreateGenericView.as_view(), name='book-listG'),
		    path('Gbooks/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-listG'),

		    # Представление на Дженериках (2-й вид) ListCreateAPIView, RetrieveUpdateDestroyAPIView
		    path('G2_books/', BookListCreateGenericView2.as_view(), name='book-listG2'),
		    path('G2_books/<int:pk>/', BookDetailUpdateDestroyView2.as_view(), name='book-listG2'),
		]
		...








Вывод:
	Можно писать представление на
	- viewsets.ModelViewSet (попробовал @action)
		( class BookViewSet(viewsets.ModelViewSet): )

		Можно быстро накидать представление, ендпоинты создаются автоматически
		get		http://127.0.0.1:8000/api/books/
		post	POST http://127.0.0.1:8000/api/books/
		get	http://127.0.0.1:8000/api/books/5/
		delete	http://127.0.0.1:8000/api/books/11/
		patch	http://127.0.0.1:8000/api/books/13/
		put	 http://127.0.0.1:8000/api/books/12/

		@action добавил (последние 5 книг)
		get http://127.0.0.1:8000/api/books/latest/
	- APIView (самый гибкий, но долгий способ)
	- 1-й вид Дженериков: ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
    - 2-й вид Дженериков: ListCreateAPIView, RetrieveUpdateDestroyAPIView




	+--------------------------------------------+-----------+-----------+------------------+-------------------+-----------+------------+
	|                  Фича                      | APIView   | ViewSet   | GenericViewSet   | ModelViewSet      | generics  |   generics  |
	|                                            |   🎯 мой  |  НЕписал  | НЕписал          |   🎯мой           | 1-й вид   |   2-й вид  |
	+--------------------------------------------+-----------+-----------+------------------+-------------------+-----------+-------------+
	| Один класс = один URL                      |     ✅    |     ❌    |        ❌        |        ❌        |           |             |
	| Группировка методов                        |     ❌    |     ✅    |        ✅        |        ✅        |           |             |
	| Автоматическая маршрутизация через роутеры |     ❌    |     ✅    |        ✅        |        ✅        |           |             |
	| Методы дженериков (get_serializer и т.п.)  |     ❌    |     ❌    |        ✅        |        ✅        |           |             |
	| Полный CRUD "из коробки"                   |     ❌    |     ❌    |        ❌        |        ✅        |           |             |
	+--------------------------------------------+-----------+------------+------------------+------------------+-----------+-------------+

    Я не пойму, если я хочу быстро все написать:
    	я пишу на ModelViewSet

	если я хочу свою собственную логику:
		я пишу на APIView

	если, я не знаю когда, мне нужно что-то промежуночное я пишу:
		на ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

	ну зачем еще
		ListCreateAPIView, RetrieveUpdateDestroyAPIView?

	при каких обстоятельствах, будет принято решение не писать на ModelViewSet не писать на APIView, не писать на ListAPIView и т.п., а писать именно на ListCreateAPIView и RetrieveUpdateDestroyAPIView?

		-Когда, я Не хочу  использовать роутеры (DefaultRouter)
		-Если я хочу полный контроль над URL, не хочу автоматической маршрутизации от ViewSet, то дженерики — лучший выбор.
		- Хочешь явно разделить права доступа, пермишены, версионность API

Все View на одной странице
	from rest_framework import viewsets, status
	from rest_framework.response import Response

	from .models import Book
	from .serializers import BookSerializer
	from rest_framework.decorators import action
	from rest_framework.views import APIView
	from django.shortcuts import get_object_or_404
	from rest_framework.generics import (
	    ListAPIView,
	    RetrieveAPIView,
	    CreateAPIView,
	    UpdateAPIView,
	    DestroyAPIView,
	    ListCreateAPIView,
	    RetrieveUpdateDestroyAPIView
	)


	"""
	Представления на разных видах View
	    -viewsets.ModelViewSet (+доп.маршрут через @action)
	    -APIView
	    -1-й вид Дженериков: ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
	    -2-й вид Дженериков: ListCreateAPIView, RetrieveUpdateDestroyAPIView
	"""


	class BookViewSet(viewsets.ModelViewSet):
	    """
	        ViewSet для модели Book. Обеспечивает стандартные операции:
	        - GET /books/ (список)
	        - POST /books/
	        - GET /books/{id}/ (детали)
	        - PUT /books/{id}/
	        - DELETE /books/{id}/
	        - PATCH
	    """
	    queryset = Book.objects.all().order_by('-id')
	    serializer_class = BookSerializer

	    @action(detail=False, methods=['get'], url_path='latest')
	    def latest_books(self, request):
	        """
	       Возвращает последние 5 книг
	       GET /books/latest/
	       """
	        books = Book.objects.order_by('-year_of_release')[:5]
	        serializer = self.get_serializer(books, many=True)
	        return Response(serializer.data, status=status.HTTP_200_OK)


	class BookListCreateAPIView(APIView):
	    """
	    Второй способ реализации-APIView
	    Вывод всех книг, поиск по title, создание книги
	    """

	    def get(self, request, *args, **kwargs):
	        books = Book.objects.order_by('-id')
	        search = request.query_params.get('search')
	        if search:
	            print('[!] search:', search)
	            books = books.filter(title__icontains=search)

	        return Response(
	            BookSerializer(books, many=True).data, status=status.HTTP_200_OK
	        )

	    def post(self, request):
	        serializer = BookSerializer(data=request.data)

	        if serializer.is_valid():
	            serializer.save()
	            return Response(serializer.data, status=status.HTTP_201_CREATED)
	        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	class BookDetailAPIView(APIView):
	    """
	    Второй способ реализации-APIView
	    POST, GET (/books/{id}/), PUT, PATCH, DELETE

	    """

	    def get_object(self, pk):
	        """
	        Вспомогательный метод: пытается найти книгу по ID (pk)
	        Если не найдена — возвращает None
	        """
	        return get_object_or_404(Book, pk=pk)

	        # try:
	        #     return Book.objects.get(pk=pk)
	        # except Book.DoesNotExist:
	        #     return None

	    def get(self, request, pk):
	        """
	        GET /api/Abooks/{id}/
	        Возвращает данные о конкретной книге по id
	        """
	        book = self.get_object(pk)
	        if not book:
	            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
	        serializer = BookSerializer(book).data
	        return Response(serializer, status=status.HTTP_200_OK)

	    def delete(self, request, pk):
	        """
	        DELETE /api/Abooks/{id}/
	        Удаляет книгу
	        """
	        book = self.get_object(pk)
	        if not book:
	            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
	        book.delete()
	        return Response(status=status.HTTP_204_NO_CONTENT)

	    def put(self, request, pk):
	        """
	        PUT /api/Abooks/{id}/
	        Полное обновление данных книги
	        """
	        book = self.get_object(pk)
	        if not book:
	            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
	        serializer = BookSerializer(book, data=request.data)
	        if serializer.is_valid():
	            serializer.save()
	            return Response(serializer.data, status=status.HTTP_200_OK)
	        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	    def patch(self, request, pk):
	        """
	        PATCH /api/Abooks/{id}/
	        Частичное обновление (можно обновить только одно поле)
	        """
	        book = self.get_object(pk)
	        if not book:
	            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)
	        serializer = BookSerializer(book, data=request.data, partial=True)  # Частичное обновление
	        if serializer.is_valid():
	            serializer.save()
	            return Response(serializer.data, status=status.HTTP_200_OK)
	        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	class BookListCreateGenericView(ListAPIView, CreateAPIView):
	    queryset = Book.objects.all().order_by('-id')
	    serializer_class = BookSerializer

	    """
	    ❓ Можно ли удалить методы get() и post()?
	    да, можно!
	    Потому что:
	        ListAPIView уже имеет метод get(), который вызывает self.list(...)
	        CreateAPIView уже имеет метод post(), который вызывает self.create(...)
	    """
	    # def get(self, request, *args, **kwargs):
	    #     return self.list(request, *args, **kwargs)
	    #
	    # def post(self, request, *args, **kwargs):
	    #     return self.create(request, *args, **kwargs)


	class BookDetailUpdateDeleteView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
	    queryset = Book.objects.all()
	    serializer_class = BookSerializer

	    # def get(self, request, *args, **kwargs):
	    #     return self.retrieve(request, *args, **kwargs)
	    #
	    # def put(self, request, *args, **kwargs):
	    #     return self.update(request, *args, **kwargs)

	    # def patch(self, request, *args, **kwargs):
	    #     return self.partial_update(request, *args, **kwargs)  # partial=True по умолчанию

	    # def delete(self, request, *args, **kwargs):
	    #     return self.destroy(request, *args, **kwargs)


	class BookListCreateGenericView2(ListCreateAPIView):
	    queryset = Book.objects.all().order_by('-id')
	    serializer_class = BookSerializer

	class BookDetailUpdateDestroyView2(RetrieveUpdateDestroyAPIView):
	    queryset = Book.objects.all()
	    serializer_class = BookSerializer

✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅

pip freeze > requiremets.txt
touch .gitignore
	.gitignore
		# Byte-compiled / optimized / DLL files
		__pycache__/
		*.py[cod]
		*$py.class

		# C extensions
		*.so

		# Distribution / packaging
		.Python
		build/
		develop-eggs/
		dist/
		downloads/
		eggs/
		.eggs/
		lib/
		lib64/
		parts/
		sdist/
		var/
		wheels/
		share/python-wheels/
		*.egg-info/
		.installed.cfg
		*.egg
		MANIFEST

		# PyInstaller
		#  Usually these files are written by a python script from a template
		#  before PyInstaller builds the exe, so as to inject date/other infos into it.
		*.manifest
		*.spec

		# Installer logs
		pip-log.txt
		pip-delete-this-directory.txt

		# Unit test / coverage reports
		htmlcov/
		.tox/
		.nox/
		.coverage
		.coverage.*
		.cache
		nosetests.xml
		coverage.xml
		*.cover
		*.py,cover
		.hypothesis/
		.pytest_cache/
		cover/

		# Translations
		*.mo
		*.pot

		# Django stuff:
		*.log
		local_settings.py
		db.sqlite3
		db.sqlite3-journal

		# Flask stuff:
		instance/
		.webassets-cache

		# Scrapy stuff:
		.scrapy

		# Sphinx documentation
		docs/_build/

		# PyBuilder
		.pybuilder/
		target/

		# Jupyter Notebook
		.ipynb_checkpoints

		# IPython
		profile_default/
		ipython_config.py

		# pyenv
		#   For a library or package, you might want to ignore these files since the code is
		#   intended to run in multiple environments; otherwise, check them in:
		# .python-version

		# pipenv
		#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
		#   However, in case of collaboration, if having platform-specific dependencies or dependencies
		#   having no cross-platform support, pipenv may install dependencies that don't work, or not
		#   install all needed dependencies.
		#Pipfile.lock

		# UV
		#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
		#   This is especially recommended for binary packages to ensure reproducibility, and is more
		#   commonly ignored for libraries.
		#uv.lock

		# poetry
		#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
		#   This is especially recommended for binary packages to ensure reproducibility, and is more
		#   commonly ignored for libraries.
		#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
		#poetry.lock

		# pdm
		#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
		#pdm.lock
		#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
		#   in version control.
		#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
		.pdm.toml
		.pdm-python
		.pdm-build/

		# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
		__pypackages__/

		# Celery stuff
		celerybeat-schedule
		celerybeat.pid

		# SageMath parsed files
		*.sage.py

		# Environments
		.env
		.venv
		env/
		venv/
		ENV/
		env.bak/
		venv.bak/

		# Spyder project settings
		.spyderproject
		.spyproject

		# Rope project settings
		.ropeproject

		# mkdocs documentation
		/site

		# mypy
		.mypy_cache/
		.dmypy.json
		dmypy.json

		# Pyre type checker
		.pyre/

		# pytype static type analyzer
		.pytype/

		# Cython debug symbols
		cython_debug/

		# PyCharm
		#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
		#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
		#  and can be added to the global gitignore or merged into this file.  For a more nuclear
		#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
		.idea/

		# PyPI configuration file
		.pypirc


		.DS_Store


git

🚸 🚸 🚸 🚸 🚸 🚸 🚸 Памятка pre-commit 🚸 🚸 🚸 🚸 🚸 🚸 🚸

pip install pre-commit
pre-commit install		✅ Это настроит автоматический запуск хуков при каждом git commit.

Использование
	git add .
	git commit -m "Test pre-commit" 		✅ Сработает на этом шаге, повторять эти шаги, пока ошибки не исчезнут


		🧠 Полезные команды
	pre-commit install          	-Устанавливает git hook
	pre-commit run              	-Запускает все хуки вручную
	pre-commit run --all-files    	-Прогоняет все файлы через проверки
	pre-commit uninstall        	 -Удаляет git hook
	git commit -m "Твой комментарий к коммиту" --no-verify        	 -Обход pre-commit

touch .pre-commit-config.yaml

.pre-commit-config.yaml (❕добавил в исключение папку notes/)
	repos:
	  - repo: https://github.com/pre-commit/pre-commit-hooks
	    rev: v4.4.0
	    hooks:
	      - id: trailing-whitespace
	      - id: end-of-file-fixer
	      - id: check-yaml
	      - id: check-json

	  - repo: https://github.com/psf/black
	    rev: 23.9.1
	    hooks:
	      - id: black
	        require_serial: true
	        exclude: ^notes/

	  - repo: https://github.com/pre-commit/mirrors-isort
	    rev: v5.10.1
	    hooks:
	      - id: isort
	        args: [ "--profile", "black" ]
	        exclude: ^notes/

	  - repo: https://github.com/PyCQA/flake8
	    rev: 6.1.0
	    hooks:
	      - id: flake8
	        args: [--max-line-length=200]
	        exclude:
	          '^notes/|
	          ^models_app/admin/__init__.py|
	          ^models_app/models/__init__.py|
	          ^models_app/migrations/'

	  - repo: https://github.com/asottile/pyupgrade
	    rev: v3.11.0
	    hooks:
	      - id: pyupgrade
	        exclude: ^notes/



	#trailing-whitespace
	#  проверки конечных пробелов

	#end-of-file-fixer
	#  Следит за тем, чтобы файлы заканчивались новой строкой и только новой строкой.

	#check-yaml
	#  Пытается загрузить все файлы YAML для проверки синтаксиса.

	#check-json
	#  Пытается загрузить все файлы JSON для проверки синтаксиса.

	#black
	#  единый стиль кода, форматирование, единообразие

	#isort
	#  для сортировки импорта в алфавитном порядке и автоматического разделения на разделы и по типу.

	#pyupgrade
	#  для автоматического обновления синтаксиса для новых версий языка.


Можно также игнорировать отдельные файлы:
	exclude: notes/training_serializer.py
	exclude: 'notes/.*\.py'  # Игнорирует все .py в папке notes

		🧠 Объяснение регулярки:
	^notes/ 	-Начинается с notes/→ игнорируем всю папку
	^models_app/admin/__init__.py	 -точный путь к файлу
	^models_app/migrations/	 -вся папка migrations


🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸 🚸

touch README.md
