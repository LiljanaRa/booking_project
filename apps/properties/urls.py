from django.urls import path

from apps.properties.views.property import (
    PropertyListCreateView,
    PropertyDetailUpdateDeleteView,
    UserPropertiesView
)

urlpatterns = [
    path('', PropertyListCreateView.as_view()),
    path('<int:pk>/', PropertyDetailUpdateDeleteView.as_view()),
    path('owner/', UserPropertiesView.as_view()),
]
