from rest_framework import serializers
from django.contrib.auth.models import User
from .user import UserSerializer
from ..models import Book, Reservation


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ReservationBaseSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, source='book'
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = Reservation
        fields = ['id', 'book', 'book_id', 'user', 'user_id', 'reservation_date', 'status']


class ReservationSerializer(ReservationBaseSerializer):
    class Meta(ReservationBaseSerializer.Meta):
        read_only_fields = ['reservation_date', 'status']


class AdminReservationSerializer(ReservationBaseSerializer):
    class Meta(ReservationBaseSerializer.Meta):
        fields = '__all__'