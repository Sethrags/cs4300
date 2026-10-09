# Generated manually for the initial booking application schema.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("release_date", models.DateField()),
                ("duration", models.PositiveIntegerField(help_text="Runtime in minutes")),
            ],
            options={"ordering": ["release_date", "title"]},
        ),
        migrations.CreateModel(
            name="Seat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("seat_number", models.CharField(max_length=10)),
                ("is_booked", models.BooleanField(default=False)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="seats", to="bookings.movie")),
            ],
            options={"ordering": ["seat_number"]},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("booking_date", models.DateTimeField(auto_now_add=True)),
                ("movie", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to="bookings.movie")),
                ("seat", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="booking", to="bookings.seat")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-booking_date"]},
        ),
        migrations.AddConstraint(
            model_name="seat",
            constraint=models.UniqueConstraint(fields=("movie", "seat_number"), name="unique_movie_seat"),
        ),
    ]
