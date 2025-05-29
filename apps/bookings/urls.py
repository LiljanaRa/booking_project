from django.urls import path

from apps.bookings.views import (
    BookingListCreateView,
    LandlordBookingListView,
    BookingDetailUpdateDeleteView,
    BookingStatusUpdateView
)

urlpatterns = [
    path('', BookingListCreateView.as_view()),
    path('landlord/', LandlordBookingListView.as_view()),
    path('<int:pk>/', BookingDetailUpdateDeleteView.as_view()),
    path('<int:pk>/status/', BookingStatusUpdateView.as_view()),
]
