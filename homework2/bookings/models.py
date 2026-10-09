from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


SEAT_NUMBER_VALIDATOR = RegexValidator(
    regex=r"^[A-Z][0-9]{1,2}$",
    message="Use a seat number such as A1 or C12.",
)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(
        help_text="Runtime in minutes",
        validators=[MinValueValidator(1), MaxValueValidator(600)],
    )

    class Meta:
        ordering = ["release_date", "title"]

    def __str__(self):
        return self.title


class Seat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=3, validators=[SEAT_NUMBER_VALIDATOR])
    is_booked = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["movie", "seat_number"], name="unique_movie_seat")]
        ordering = ["seat_number"]

    def __str__(self):
        return f"{self.movie}: {self.seat_number}"


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    seat = models.OneToOneField(Seat, on_delete=models.PROTECT, related_name="booking")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booking_date"]

    def clean(self):
        if self.seat_id and self.movie_id and self.seat.movie_id != self.movie_id:
            raise ValidationError("The selected seat does not belong to this movie.")

    def __str__(self):
        return f"{self.user} - {self.movie} ({self.seat.seat_number})"
