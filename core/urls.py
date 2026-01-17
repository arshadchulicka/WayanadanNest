from django.urls import path
from .views import home, contact_us, find_us

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact_us, name='contact'),
    path('find-us/', find_us, name='find_us'),
]
