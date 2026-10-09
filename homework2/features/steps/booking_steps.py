from datetime import date

from behave import given, then, when
from django.contrib.auth import get_user_model
from django.urls import reverse

from bookings.models import Booking, Movie, Seat


@given('a movie named "{title}" with an available seat "{seat_number}"')
def create_movie_with_seat(context, title, seat_number):
    context.movie = Movie.objects.create(
        title=title,
        description="Created for a BDD scenario.",
        release_date=date(2026, 1, 1),
        duration=100,
    )
    context.seat = Seat.objects.create(movie=context.movie, seat_number=seat_number)


@given('a registered moviegoer named "{username}"')
def create_moviegoer(context, username):
    context.username = username
    context.password = "safe-password"
    get_user_model().objects.create_user(username=username, password=context.password)


@when("I visit the movie catalogue")
def visit_catalogue(context):
    context.response = context.test.client.get(reverse("movie-list"))


@when("the moviegoer signs in")
def sign_in(context):
    context.test.client.login(username=context.username, password=context.password)


@when('the moviegoer reserves seat "{seat_number}"')
def reserve_seat(context, seat_number):
    context.response = context.test.client.post(
        reverse("book-seat", args=[context.movie.id]), {"seat": context.seat.id}
    )


@then("the response status is {status_code:d}")
def response_has_status(context, status_code):
    assert context.response.status_code == status_code


@then('I see "{text}"')
def response_contains_text(context, text):
    assert text in context.response.content.decode()


@then('the reservation is recorded for "{username}"')
def reservation_is_recorded(context, username):
    booking = Booking.objects.get(movie=context.movie, seat=context.seat)
    assert booking.user.username == username


@then('seat "{seat_number}" is marked as booked')
def seat_is_booked(context, seat_number):
    context.seat.refresh_from_db()
    assert context.seat.seat_number == seat_number
    assert context.seat.is_booked is True
