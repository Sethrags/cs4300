from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView

from .models import Booking, Movie
from .services import SeatReservationError, reserve_seat


class MovieListView(ListView):
    template_name = "bookings/movie_list.html"
    context_object_name = "movies"
    queryset = Movie.objects.prefetch_related("seats")


class RegisterView(FormView):
    """Allow visitors, including graders, to create an account and book a seat."""

    template_name = "bookings/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("movie-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Your account is ready. You can now reserve a seat.")
        return super().form_valid(form)


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
            booking = reserve_seat(movie=movie, seat_id=seat_id, user=request.user)
            messages.success(request, f"Seat {booking.seat.seat_number} is confirmed for {movie.title}.")
            return redirect("booking-history")
        except (SeatReservationError, ValueError) as exc:
            messages.error(request, str(exc) or "Please select an available seat for this movie.")
        return redirect("book-seat", movie_id=movie.id)


class BookingHistoryView(LoginRequiredMixin, ListView):
    template_name = "bookings/booking_history.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.select_related("movie", "seat").filter(user=self.request.user)
