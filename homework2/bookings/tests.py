from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Booking, Movie, Seat


class BookingModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("alex", password="safe-password")
        self.movie = Movie.objects.create(title="Test Feature", description="A test movie.", release_date=date(2026, 1, 1), duration=100)
        self.seat = Seat.objects.create(movie=self.movie, seat_number="A1")

    def test_a_seat_can_only_have_one_booking(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertTrue(self.seat.booking)

    def test_booking_rejects_a_seat_from_another_movie(self):
        other_movie = Movie.objects.create(
            title="Other Feature",
            description="A second test movie.",
            release_date=date(2026, 2, 1),
            duration=95,
        )
        other_seat = Seat.objects.create(movie=other_movie, seat_number="B1")
        booking = Booking(movie=self.movie, seat=other_seat, user=self.user)

        with self.assertRaisesMessage(Exception, "does not belong"):
            booking.full_clean()

    def test_model_string_representations_are_readable(self):
        self.assertEqual(str(self.movie), "Test Feature")
        self.assertEqual(str(self.seat), "Test Feature: A1")


class BookingApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("alex", password="safe-password")
        self.movie = Movie.objects.create(title="Test Feature", description="A test movie.", release_date=date(2026, 1, 1), duration=100)
        self.seat = Seat.objects.create(movie=self.movie, seat_number="A1")
        self.client = APIClient()

    def test_movies_are_publicly_listed(self):
        response = self.client.get(reverse("movie-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.movie.title)

    def test_api_lists_available_seats(self):
        response = self.client.get("/api/seats/available/?movie=" + str(self.movie.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["status"], "available")

    def test_seats_can_be_filtered_by_movie_and_booked_seats_are_hidden(self):
        other_movie = Movie.objects.create(
            title="Other Feature",
            description="A second test movie.",
            release_date=date(2026, 2, 1),
            duration=95,
        )
        other_seat = Seat.objects.create(movie=other_movie, seat_number="B1")
        self.seat.is_booked = True
        self.seat.save(update_fields=["is_booked"])

        filtered = self.client.get(f"/api/seats/?movie={other_movie.id}")
        available = self.client.get(f"/api/seats/available/?movie={self.movie.id}")

        self.assertEqual(filtered.status_code, status.HTTP_200_OK)
        self.assertEqual([seat["id"] for seat in filtered.data], [other_seat.id])
        self.assertEqual(available.data, [])

    def test_unauthenticated_users_cannot_create_movies_or_bookings(self):
        movie_response = self.client.post(
            "/api/movies/",
            {
                "title": "Unauthorized",
                "description": "Should not be added.",
                "release_date": "2026-03-01",
                "duration": 90,
            },
            format="json",
        )
        booking_response = self.client.post(
            "/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id}, format="json"
        )

        self.assertEqual(movie_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(booking_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_book_an_available_seat(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booked_seat_is_rejected(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.seat.is_booked = True
        self.seat.save()
        other_user = get_user_model().objects.create_user("sam", password="safe-password")
        self.client.force_authenticate(other_user)
        response = self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seat_from_a_different_movie_is_rejected(self):
        other_movie = Movie.objects.create(
            title="Other Feature",
            description="A second test movie.",
            release_date=date(2026, 2, 1),
            duration=95,
        )
        other_seat = Seat.objects.create(movie=other_movie, seat_number="B1")
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/api/bookings/", {"movie": self.movie.id, "seat": other_seat.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not assigned", str(response.data))

    def test_user_only_sees_their_own_history(self):
        other_user = get_user_model().objects.create_user("sam", password="safe-password")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=other_user)
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_cancelling_a_booking_reopens_its_seat(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.seat.is_booked = True
        self.seat.save(update_fields=["is_booked"])
        self.client.force_authenticate(self.user)

        response = self.client.delete(f"/api/bookings/{booking.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)
        self.assertFalse(Booking.objects.filter(pk=booking.id).exists())


class BookingViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("alex", password="safe-password")
        self.movie = Movie.objects.create(
            title="Test Feature",
            description="A test movie.",
            release_date=date(2026, 1, 1),
            duration=100,
        )
        self.seat = Seat.objects.create(movie=self.movie, seat_number="A1")

    def test_booking_page_requires_login(self):
        response = self.client.get(reverse("book-seat", args=[self.movie.id]))

        self.assertRedirects(
            response,
            f"/accounts/login/?next=/movies/{self.movie.id}/book/",
            fetch_redirect_response=False,
        )

    def test_logged_in_user_can_book_from_the_web_page(self):
        self.client.login(username="alex", password="safe-password")

        response = self.client.post(reverse("book-seat", args=[self.movie.id]), {"seat": self.seat.id})

        self.assertRedirects(response, reverse("booking-history"), fetch_redirect_response=False)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)
        self.assertEqual(Booking.objects.get().user, self.user)

    def test_unknown_movie_returns_not_found(self):
        self.client.login(username="alex", password="safe-password")

        response = self.client.get(reverse("book-seat", args=[9999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
