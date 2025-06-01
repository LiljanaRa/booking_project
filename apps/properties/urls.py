from django.urls import path

from apps.properties.views.rent_property import (
    PropertyListCreateView,
    PropertyDetailUpdateDeleteView,
    UserPropertiesView,
    SwitchPropertyActiveStatusView,
    PropertyBookingsView,
    PropertyUnavailableDatesView,
    PopularPropertyListView,
    PopularSearchKeywordsView
)
from apps.properties.views.review import (
    ReviewCreateView,
    ReviewUpdateDeleteView,
    PropertyReviewListView,
)

urlpatterns = [
    path('', PropertyListCreateView.as_view()),
    path('<int:pk>/', PropertyDetailUpdateDeleteView.as_view()),
    path('<int:pk>/switch-active/', SwitchPropertyActiveStatusView.as_view()),
    path('owner/', UserPropertiesView.as_view()),
    path('reviews/', ReviewCreateView.as_view()),
    path('reviews/<int:pk>/', ReviewUpdateDeleteView.as_view()),
    path('<int:rent_property_id>/reviews/', PropertyReviewListView.as_view()),
    path('<int:rent_property_id>/bookings/', PropertyBookingsView.as_view()),
    path('<int:rent_property_id>/unavailable-dates/', PropertyUnavailableDatesView.as_view()),
    path('popular/', PopularPropertyListView.as_view()),
    path('search/popular/', PopularSearchKeywordsView.as_view()),
]
