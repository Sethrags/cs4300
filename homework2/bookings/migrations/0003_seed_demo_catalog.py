from datetime import date
import re

from django.db import migrations


def seed_demo_catalog(apps, schema_editor):
    """Remove legacy invalid records and provide a realistic demo for an empty catalogue."""
    Booking = apps.get_model("bookings", "Booking")
    Movie = apps.get_model("bookings", "Movie")
    Seat = apps.get_model("bookings", "Seat")

    invalid_movie_ids = list(Movie.objects.filter(duration__gt=600).values_list("id", flat=True))
    if invalid_movie_ids:
        Booking.objects.filter(movie_id__in=invalid_movie_ids).delete()
        Movie.objects.filter(id__in=invalid_movie_ids).delete()

    invalid_seat_ids = [
        seat.id for seat in Seat.objects.all() if not re.fullmatch(r"[A-Z][0-9]{1,2}", seat.seat_number)
    ]
    if invalid_seat_ids:
        Booking.objects.filter(seat_id__in=invalid_seat_ids).delete()
        Seat.objects.filter(id__in=invalid_seat_ids).delete()

    if Movie.objects.exists():
        return

    movies = [
        (
            "Aurora Lane",
            "A night-shift radio host follows a signal that seems to predict the city’s future.",
            date(2026, 4, 10),
            108,
        ),
        (
            "The Last Mapmaker",
            "An apprentice cartographer sets out to chart an island that appears only once a decade.",
            date(2026, 5, 22),
            116,
        ),
        (
            "Second Sunrise",
            "Two estranged siblings race to restore a solar observatory before a rare celestial event.",
            date(2026, 6, 5),
            102,
        ),
    ]

    for title, description, release_date, duration in movies:
        movie = Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            duration=duration,
        )
        Seat.objects.bulk_create(
            [Seat(movie=movie, seat_number=f"{row}{number}") for row in ("A", "B") for number in range(1, 7)]
        )


class Migration(migrations.Migration):
    dependencies = [("bookings", "0002_validate_movie_duration_and_seat_number")]

    operations = [migrations.RunPython(seed_demo_catalog, migrations.RunPython.noop)]
