from django.db import IntegrityError, transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


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


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.select_related("movie", "seat", "user").filter(user=self.request.user)

    def perform_create(self, serializer):
        """Reserve a seat atomically so two clients cannot book it simultaneously."""
        try:
            with transaction.atomic():
                seat = Seat.objects.select_for_update().get(pk=serializer.validated_data["seat"].pk)
                if seat.is_booked:
                    from rest_framework.exceptions import ValidationError
                    raise ValidationError({"seat": "This seat has already been booked."})
                if seat.movie_id != serializer.validated_data["movie"].pk:
                    from rest_framework.exceptions import ValidationError
                    raise ValidationError({"seat": "This seat is not assigned to the selected movie."})
                serializer.save(user=self.request.user, seat=seat)
                seat.is_booked = True
                seat.save(update_fields=["is_booked"])
        except IntegrityError:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"seat": "This seat has already been booked."})

    def perform_destroy(self, instance):
        with transaction.atomic():
            seat = Seat.objects.select_for_update().get(pk=instance.seat_id)
            instance.delete()
            seat.is_booked = False
            seat.save(update_fields=["is_booked"])
