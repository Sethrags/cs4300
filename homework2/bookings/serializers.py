from rest_framework import serializers

from .models import Booking, Movie, Seat


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ["id", "movie", "movie_title", "seat_number", "is_booked", "status"]
        read_only_fields = ["is_booked"]

    def get_status(self, obj):
        return "booked" if obj.is_booked else "available"


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    seat_number = serializers.CharField(source="seat.seat_number", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "movie", "movie_title", "seat", "seat_number", "user", "user_id", "booking_date"]
        read_only_fields = ["booking_date"]

    def validate(self, attrs):
        movie = attrs["movie"]
        seat = attrs["seat"]
        if seat.movie_id != movie.id:
            raise serializers.ValidationError({"seat": "This seat is not assigned to the selected movie."})
        return attrs
