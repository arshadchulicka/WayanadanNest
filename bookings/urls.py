from django.urls import path
from .views import create_booking
from . import views
urlpatterns = [
    path("my/", views.my_bookings, name="my_bookings"),
    path('create/<int:resort_id>/', views.create_booking, name='create_booking'),
    path('summary/<int:booking_id>/', views.booking_summary, name='booking_summary'),
]
