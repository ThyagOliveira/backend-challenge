from rest_framework import serializers
from ..models import Book, Reservation


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AdminReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['book', 'user', 'reservation_date', 'status']
        read_only_fields = ['reservation_date', 'status']
