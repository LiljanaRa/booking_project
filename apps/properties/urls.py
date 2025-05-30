from django.urls import path

from apps.properties.views.property import (
    PropertyListCreateView,
    PropertyDetailUpdateDeleteView,
    UserPropertiesView,
    SwitchPropertyActiveStatusView
)

urlpatterns = [
    path('', PropertyListCreateView.as_view()),
    path('<int:pk>/', PropertyDetailUpdateDeleteView.as_view()),
    path('<int:pk>/switch-active/', SwitchPropertyActiveStatusView.as_view()),
    path('owner/', UserPropertiesView.as_view()),
]
