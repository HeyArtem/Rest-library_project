from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer

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

    queryset = Book.objects.all().order_by("-id")
    serializer_class = BookSerializer

    @action(detail=False, methods=["get"], url_path="latest")
    def latest_books(self, request):
        """
        Возвращает последние 5 книг
        GET /books/latest/
        """
        books = Book.objects.order_by("-year_of_release")[:5]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookListCreateAPIView(APIView):
    """
    Второй способ реализации-APIView
    Вывод всех книг, поиск по title, создание книги
    """

    def get(self, request, *args, **kwargs):
        books = Book.objects.order_by("-id")
        search = request.query_params.get("search")
        if search:
            print("[!] search:", search)
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
            return Response(
                {"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookSerializer(book).data
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        DELETE /api/Abooks/{id}/
        Удаляет книгу
        """
        book = self.get_object(pk)
        if not book:
            return Response(
                {"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        """
        PUT /api/Abooks/{id}/
        Полное обновление данных книги
        """
        book = self.get_object(pk)
        if not book:
            return Response(
                {"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
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
            return Response(
                {"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookSerializer(
            book, data=request.data, partial=True
        )  # Частичное обновление
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateGenericView(ListAPIView, CreateAPIView):
    queryset = Book.objects.all().order_by("-id")
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
    queryset = Book.objects.all().order_by("-id")
    serializer_class = BookSerializer


class BookDetailUpdateDestroyView2(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
