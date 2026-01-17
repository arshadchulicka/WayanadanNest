from django.urls import path
from .views import pay_now, payment_success
from . import views
urlpatterns = [
    
    path('pay/<int:booking_id>/', views.pay_now, name='pay_now'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
]
