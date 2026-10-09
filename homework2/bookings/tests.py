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

    def test_user_only_sees_their_own_history(self):
        other_user = get_user_model().objects.create_user("sam", password="safe-password")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=other_user)
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
