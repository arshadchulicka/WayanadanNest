
from resorts.models import Resort
from .models import Carousel
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage
from django.contrib import messages
from django.db.models import Avg
def home(request):
    carousel_images = Carousel.objects.filter(is_active=True)
    resorts = Resort.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ) 
    return render(request, 'core/home.html', {
        'resorts': resorts,
        'carousel_images': carousel_images,
        'discount': settings.NEW_YEAR_DISCOUNT_PERCENT,

        })


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Save to DB
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            # Send Email
            send_mail(
                subject=f"New Contact Message from {name}",
                message=f"From: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')

    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
from .models import CompanyInfo
def find_us(request):
    company = CompanyInfo.objects.first()  # single record
    return render(request, 'core/find_us.html', {
        'company': company
    })