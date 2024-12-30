import csv
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUploadView(APIView):

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            csv_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(csv_file)
            books = []

            success_count = 0
            error_count = 0
            errors = []

            for row in reader:
                try:
                    book = Book(
                        goodreads_book_id=row['goodreads_book_id'],
                        best_book_id=row['best_book_id'],
                        work_id=row['work_id'],
                        books_count=row['books_count'],
                        isbn=row['isbn'],
                        isbn13=row['isbn13'],
                        authors=row['authors'],
                        original_publication_year=row['original_publication_year'],
                        original_title=row['original_title'],
                        title=row['title'],
                        language_code=row['language_code'],
                        average_rating=row['average_rating'],
                        ratings_count=row['ratings_count'],
                        work_ratings_count=row['work_ratings_count'],
                        work_text_reviews_count=row['work_text_reviews_count'],
                        ratings_1=row['ratings_1'],
                        ratings_2=row['ratings_2'],
                        ratings_3=row['ratings_3'],
                        ratings_4=row['ratings_4'],
                        ratings_5=row['ratings_5'],
                        image_url=row['image_url'],
                        small_image_url=row['small_image_url'],
                    )

                    books.append(book)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"Error processing book {row['title']}: {str(e)}")

            Book.objects.bulk_create(books)
            
            send_mail(
                'CSV Ingestion Report',
                f'Successfully ingested {success_count} books.\nErrors: {error_count}\n{errors}',
                'from@example.com',
                ['admin@example.com'],
            )

            return Response({
                "message": f"Successfully processed {success_count} books.",
                "errors": errors
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        