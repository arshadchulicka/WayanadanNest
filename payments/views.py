from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from .models import Payment
from reviews.models import Review
from django.conf import settings


@login_required
def pay_now(request, booking_id):
    booking = get_object_or_404(
        Booking, id=booking_id, user=request.user
    )

    # Prevent double payment
    if hasattr(booking, 'payment') and booking.payment.status == 'PAID':
        return redirect('payment_success', booking.id)

    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={'amount': booking.total_amount}
    )

    if request.method == 'POST':
        # ✅ FAKE PAYMENT SUCCESS
        payment.status = 'PAID'
        payment.save()

        booking.status = 'PAID'
        booking.save()

        return redirect('payment_success', booking.id)

    return render(request, 'payments/pay_now.html', {
        'booking': booking,
        'payment': payment,
        'discount_percent': settings.NEW_YEAR_DISCOUNT_PERCENT
    })



@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    payment = booking.payment

    # ✅ Mark as paid (FAKE SUCCESS)
    payment.status = 'PAID'
    payment.save()

    booking.status = 'PAID'
    booking.save()
    has_reviewed = Review.objects.filter(
        user=request.user,
        resort=booking.resort
    ).exists()
    return render(request, 'payments/payment_success.html', {
        'booking': booking,
        'has_reviewed': has_reviewed
    })
