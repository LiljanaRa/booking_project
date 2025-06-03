from django.urls import path

from apps.bookings.views import (
    BookingListCreateView,
    LandlordBookingListView,
    BookingDetailUpdateDeleteView,
    BookingStatusUpdateView,
    LandlordBookingView
)

urlpatterns = [
    path('', BookingListCreateView.as_view()),
    path('<int:pk>/', BookingDetailUpdateDeleteView.as_view()),
    path('<int:pk>/status/', BookingStatusUpdateView.as_view()),
    path('landlord/', LandlordBookingListView.as_view()),
    path('landlord/<int:pk>/', LandlordBookingView.as_view()),
]
