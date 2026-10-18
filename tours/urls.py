from django.urls import path

from . import views

urlpatterns = [
    path("", views.tours, name="tours"),
    path("<int:tour_id>/", views.tour_detail, name="tour_detail"),
]
