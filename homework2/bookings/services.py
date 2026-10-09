from django.db import IntegrityError, transaction

from .models import Booking, Seat


class SeatReservationError(Exception):
    """Raised when a seat cannot be reserved for a booking request."""


def reserve_seat(*, movie, seat_id, user):
    """Create a booking and mark its seat unavailable in one transaction."""
    try:
        with transaction.atomic():
            seat = Seat.objects.select_for_update().get(pk=seat_id)
            if seat.movie_id != movie.pk:
                raise SeatReservationError("This seat is not assigned to the selected movie.")
            if seat.is_booked:
                raise SeatReservationError("This seat has already been booked.")

            try:
                booking = Booking.objects.create(movie=movie, seat=seat, user=user)
            except IntegrityError as exc:
                raise SeatReservationError("This seat has already been booked.") from exc

            seat.is_booked = True
            seat.save(update_fields=["is_booked"])
            return booking
    except Seat.DoesNotExist as exc:
        raise SeatReservationError("Please select an available seat for this movie.") from exc
