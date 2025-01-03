from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from ..models import Book
from ..serializers.books import BookSerializer
from ..services.book_service import BookService
from ..permissions import IsAdminOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["title", "authors", "original_title", "original_publication_year"]


    @action(detail=False, methods=["post"])
    def upload(self,request):
        file = request.FILES.get('file')

        if not file:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            success_count, errors = BookService.bulk_create_books_from_csv(file)

            subject = 'CSV Ingestion Report'
            message = f'Successfully ingested {success_count} books.'
            if errors:
                message += f"\nErrors: {len(errors)}\n{errors}"

            send_mail(subject, message, 'from@example.com', ['admin@example.com'])

            return Response({
                "message": f"Successfully processed {success_count} books.",
                "errors": errors
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
