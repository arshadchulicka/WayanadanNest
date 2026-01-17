from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from resorts.models import Resort
from django.conf import settings




from django.db.models import Sum
from datetime import date

@login_required
def create_booking(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id, is_active=True)
    form = BookingForm(request.POST or None)

    available_rooms = resort.total_rooms  # default

    if request.method == 'POST' and form.is_valid():
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        room_count = form.cleaned_data['room_count']

        if check_in < date.today():
            messages.error(request, "Check-in date cannot be in the past.")
            return redirect(request.path)

        if check_out <= check_in:
            messages.error(request, "Check-out must be after check-in.")
            return redirect(request.path)

        # 🔁 FIND OVERLAPPING BOOKINGS
        overlapping_bookings = Booking.objects.filter(
            resort=resort,
            status='PAID',
            check_in__lt=check_out,
            check_out__gt=check_in
        )

        # 🧮 TOTAL ROOMS ALREADY BOOKED
        booked_rooms = overlapping_bookings.aggregate(
            total=Sum('room_count')
        )['total'] or 0

        available_rooms = resort.total_rooms - booked_rooms

        if room_count > available_rooms:
            messages.error(
                request,
                f"Only {available_rooms} room(s) available for selected dates."
            )
            return redirect(request.path)

        # 💰 PRICE CALCULATION
        days = (check_out - check_in).days
        discount_percent = getattr(settings, 'NEW_YEAR_DISCOUNT_PERCENT', 0)

        price = resort.price_per_night
        discounted_price = price - (price * discount_percent / 100)

        original_amount = days * room_count * price
        discount_amount = days * room_count * (price - discounted_price)
        final_amount = days * room_count * discounted_price

        booking = Booking.objects.create(
            user=request.user,
            resort=resort,
            check_in=check_in,
            check_out=check_out,
            room_count=room_count,
            original_amount=original_amount,
            discount_amount=discount_amount,
            total_amount=final_amount,
            status='PENDING'
        )

        return redirect('booking_summary', booking.id)

    context = {
        'resort': resort,
        'form': form,
        'available_rooms': available_rooms,
        'discount_percent': getattr(settings, 'NEW_YEAR_DISCOUNT_PERCENT', 0),
    }
    return render(request, 'bookings/create.html', context)



@login_required
def booking_summary(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/summary.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-id")
    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings
    })