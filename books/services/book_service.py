import csv
from ..models import Book


class BookService:
    @staticmethod
    def bulk_create_books_from_csv(file):
        csv_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(csv_file)
        books = []
        errors = []

        for row in reader:
            try:
                row.pop('book_id', None)
                books.append(Book(**row))
            except Exception as e:
                errors.append(f"Error processing book {row.get('title')}: {str(e)}")

        try:
            Book.objects.bulk_create(books)
        except Exception as e:
            errors.append(f"Error during bulk create: {e}")

        return len(books), errors