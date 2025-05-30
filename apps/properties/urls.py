from django.urls import path

from apps.properties.views.property import (
    PropertyListCreateView,
    PropertyDetailUpdateDeleteView,
    UserPropertiesView,
    SwitchPropertyActiveStatusView
)
from apps.properties.views.review import ReviewCreateView

urlpatterns = [
    path('', PropertyListCreateView.as_view()),
    path('<int:pk>/', PropertyDetailUpdateDeleteView.as_view()),
    path('<int:pk>/switch-active/', SwitchPropertyActiveStatusView.as_view()),
    path('owner/', UserPropertiesView.as_view()),
    path('reviews/', ReviewCreateView.as_view()),
]
