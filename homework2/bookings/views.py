from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from .models import Booking, Movie, Seat


class MovieListView(ListView):
    template_name = "bookings/movie_list.html"
    context_object_name = "movies"
    queryset = Movie.objects.prefetch_related("seats")


class SeatBookingView(LoginRequiredMixin, TemplateView):
    template_name = "bookings/seat_booking.html"

    def get_movie(self):
        try:
            return Movie.objects.get(pk=self.kwargs["movie_id"])
        except Movie.DoesNotExist as exc:
            raise Http404("Movie not found") from exc

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie"] = self.get_movie()
        context["seats"] = context["movie"].seats.all()
        return context

    def post(self, request, *args, **kwargs):
        movie = self.get_movie()
        try:
            seat_id = int(request.POST.get("seat", ""))
            with transaction.atomic():
                seat = Seat.objects.select_for_update().get(pk=seat_id, movie=movie)
                if seat.is_booked:
                    messages.error(request, "That seat was just booked. Please choose another one.")
                else:
                    Booking.objects.create(movie=movie, seat=seat, user=request.user)
                    seat.is_booked = True
                    seat.save(update_fields=["is_booked"])
                    messages.success(request, f"Seat {seat.seat_number} is confirmed for {movie.title}.")
                    return redirect("booking-history")
        except (Seat.DoesNotExist, ValueError, IntegrityError):
            messages.error(request, "Please select an available seat for this movie.")
        return redirect("book-seat", movie_id=movie.id)


class BookingHistoryView(LoginRequiredMixin, ListView):
    template_name = "bookings/booking_history.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.select_related("movie", "seat").filter(user=self.request.user)
