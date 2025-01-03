from django.db import transaction
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from ..models import Book, Reservation
from ..serializers.books import BookSerializer, ReservationSerializer, AdminReservationSerializer
from ..services.book_service import BookService
from ..permissions import IsAdminOrReadOnly, IsAdminOrOwner


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["title", "authors", "original_title", "original_publication_year"]

    def partial_update(self, request, pk=None):
        with transaction.atomic():
            book = Book.objects.select_for_update().get(id=pk)

            if not book:
                raise ValidationError('Book not found or blocked by transaction') 

            serializer = self.get_serializer(book, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)


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


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    permissions_classes = [IsAdminOrOwner]
    
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            return AdminReservationSerializer
        return ReservationSerializer

    def post(self, request, book_id):
        try:
            reservation = BookService.reservation_book(request.user, book_id)

            return Response({
                "message": f"Book '{reservation.book.title}' Successfully reserved.",
                "reservation_id": reservation.id
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        with transaction.atomic():
            book_reservation = Reservation.objects.select_for_update().get(id=pk)

            if not book_reservation:
                raise ValidationError('Reservation not found or blocked by transaction') 

            serializer = self.get_serializer(book_reservation, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)