from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from bookings.api import BookingViewSet, MovieViewSet, SeatViewSet
from bookings import views

router = DefaultRouter()
router.register("movies", MovieViewSet)
router.register("seats", SeatViewSet, basename="seat")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="bookings/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.MovieListView.as_view(), name="movie-list"),
    path("movies/<int:movie_id>/book/", views.SeatBookingView.as_view(), name="book-seat"),
    path("bookings/", views.BookingHistoryView.as_view(), name="booking-history"),
    path("api/", include(router.urls)),
]
