from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from library_project import settings

from .views import (
    BookDetailAPIView,
    BookDetailUpdateDeleteView,
    BookDetailUpdateDestroyView2,
    BookListCreateAPIView,
    BookListCreateGenericView,
    BookListCreateGenericView2,
    BookViewSet,
)

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
# basename='book' нужен, если DRF не может сам определить имя маршрута (например, если ты не указал queryset в ViewSet


urlpatterns = [
    path("", include(router.urls)),
    # Проект на APIView
    path("Abooks/", BookListCreateAPIView.as_view(), name="book-list"),
    path("Abooks/<int:pk>/", BookDetailAPIView.as_view(), name="book-detail"),
    # Представление на Дженериках ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
    path("Gbooks/", BookListCreateGenericView.as_view(), name="book-listG"),
    path("Gbooks/<int:pk>/", BookDetailUpdateDeleteView.as_view(), name="book-listG"),
    # Представление на Дженериках (2-й вид) ListCreateAPIView, RetrieveUpdateDestroyAPIView
    path("G2_books/", BookListCreateGenericView2.as_view(), name="book-listG2"),
    path(
        "G2_books/<int:pk>/", BookDetailUpdateDestroyView2.as_view(), name="book-listG2"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
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
"""
