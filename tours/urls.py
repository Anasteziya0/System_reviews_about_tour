from django.urls import path

from . import views

app_name = "tours"

urlpatterns = [
    path("", views.tours, name="list"),
    path("<int:tour_id>/", views.tour_detail, name="detail"),
]
