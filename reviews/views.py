from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from .models import Review
from django.contrib import messages

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='PAID'

    )
    resort = booking.resort
    # Prevent duplicate review
    if Review.objects.filter(user=request.user, resort=resort).exists():
        messages.warning(request, "You have already reviewed this resort.")
        return redirect('resort_detail', resort.id)
    if not hasattr(booking, 'payment') or booking.payment.status != 'PAID':
        return redirect('home')
    if request.method == "POST":
        Review.objects.create(
            user=request.user,
            resort=booking.resort,
            booking=booking,
            rating=request.POST["rating"],
            review=request.POST["review"]
        )
        return redirect("resort_detail", booking.resort.id)

    return render(request, "reviews/add_reviews.html", {
        "booking": booking
    })
