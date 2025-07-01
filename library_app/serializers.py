from datetime import datetime

from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
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
