from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("bookings", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="duration",
            field=models.PositiveIntegerField(
                help_text="Runtime in minutes",
                validators=[MinValueValidator(1), MaxValueValidator(600)],
            ),
        ),
        migrations.AlterField(
            model_name="seat",
            name="seat_number",
            field=models.CharField(
                max_length=3,
                validators=[
                    RegexValidator(
                        message="Use a seat number such as A1 or C12.",
                        regex="^[A-Z][0-9]{1,2}$",
                    )
                ],
            ),
        ),
    ]
