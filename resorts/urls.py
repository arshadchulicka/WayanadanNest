from django.urls import path
from . import views

urlpatterns = [
    path('', views.resort_list, name='resort_list'),
    path('<int:resort_id>/', views.resort_detail, name='resort_detail'),
]
