from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer
from .services import SeatReservationError, reserve_seat


class MovieViewSet(viewsets.ModelViewSet):
    """Public movie listings; authenticated users can maintain the catalogue."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """Expose seat availability, optionally filtered with ?movie=<movie_id>."""

    serializer_class = SeatSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Seat.objects.select_related("movie")
        movie_id = self.request.query_params.get("movie")
        return queryset.filter(movie_id=movie_id) if movie_id else queryset

    @action(detail=False, methods=["get"])
    def available(self, request):
        queryset = self.get_queryset().filter(is_booked=False)
        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        """Reserve this seat through the seat API endpoint."""
        seat = self.get_object()
        try:
            booking = reserve_seat(movie=seat.movie, seat_id=seat.pk, user=request.user)
        except SeatReservationError as exc:
            raise ValidationError({"seat": str(exc)}) from exc
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.select_related("movie", "seat", "user").filter(user=self.request.user)

    def perform_create(self, serializer):
        """Reserve a seat atomically so two clients cannot book it simultaneously."""
        try:
            serializer.instance = reserve_seat(
                movie=serializer.validated_data["movie"],
                seat_id=serializer.validated_data["seat"].pk,
                user=self.request.user,
            )
        except SeatReservationError as exc:
            raise ValidationError({"seat": str(exc)}) from exc

    def perform_destroy(self, instance):
        with transaction.atomic():
            seat = Seat.objects.select_for_update().get(pk=instance.seat_id)
            instance.delete()
            seat.is_booked = False
            seat.save(update_fields=["is_booked"])
