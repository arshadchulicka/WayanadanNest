from django.shortcuts import render, get_object_or_404
from .models import Resort
from django.db.models import Avg
from django.conf import settings
from bookings.models import Booking
from reviews.models import Review
from django.db import models

def resort_list(request):
    resorts = Resort.objects.annotate(
        avg_rating=Avg('reviews__rating')
    )
    return render(request, 'resorts/resort_list.html', {
        'resorts': resorts,
        'discount': settings.NEW_YEAR_DISCOUNT_PERCENT,
        })






def resort_detail(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id)

    has_paid_booking = False
    has_reviewed = False

    if request.user.is_authenticated:
        has_paid_booking = Booking.objects.filter(
            user=request.user,
            resort=resort,
            status='PAID'
        ).exists()

        has_reviewed = Review.objects.filter(
            user=request.user,
            resort=resort
        ).exists()

    context = {
        'resort': resort,
        'has_paid_booking': has_paid_booking,
        'has_reviewed': has_reviewed,
        'avg_rating': resort.reviews.aggregate(avg=models.Avg('rating'))['avg'],
        'discount': settings.NEW_YEAR_DISCOUNT_PERCENT,
    }

    return render(request, 'resorts/resort_detail.html', context)
