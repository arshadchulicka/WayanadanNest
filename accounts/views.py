from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import email_verification_token
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User

from django.http import HttpResponse


from .models import OTP, Profile
from .utils import generate_otp


from django.utils.timezone import now
from datetime import timedelta


from django.utils.crypto import get_random_string





def user_register(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save() 
        login(request, user)
        return redirect('/')

    return render(request, 'accounts/register.html', {'form': form})





def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()

            # ✅ ENSURE PROFILE EXISTS
            profile, created = Profile.objects.get_or_create(user=user)

            # ❌ REMOVE ALL BLOCKERS FOR NOW
            # if not profile.is_email_verified:
            #     return render(request, 'accounts/login.html', {
            #         'form': form,
            #         'error': 'Please verify your email first'
            #     })

            login(request, user)
            return redirect('/')

        else:
            return render(request, 'accounts/login.html', {
                'form': form,
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('/')
@login_required
def update_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        profile.save()
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile})



def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    link = request.build_absolute_uri(
        reverse('verify_email', args=[uid, token])
    )

    send_mail(
        'Verify your email',
        f'Click to verify: {link}',
        'noreply@wayanadannest.com',
        [user.email],
    )





def verify_email(request, token):
    profile = get_object_or_404(Profile, email_verification_token=token)
    profile.is_email_verified = True
    profile.email_verification_token = ''
    profile.save()
    return render(request, 'accounts/email_verified.html')




def send_otp(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        otp_code = generate_otp()

        OTP.objects.create(phone=phone, code=otp_code)

        # TEMP: print OTP (replace with SMS API)
        print("OTP:", otp_code)

        return render(request, 'accounts/verify_otp.html', {'phone': phone})

    return render(request, 'accounts/send_otp.html')




def verify_otp(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        code = request.POST['otp']

        otp_obj = OTP.objects.filter(
            phone=phone,
            code=code,
            created_at__gte=now() - timedelta(minutes=5)
        ).last()

        if not otp_obj:
            return render(request, 'accounts/verify_otp.html', {
                'error': 'Invalid or expired OTP',
                'phone': phone
            })

        profile = Profile.objects.get(phone=phone)
        user = profile.user

        # 🔐 SAME LOGIN RULES
        if not profile.is_email_verified:
            return render(request, 'accounts/verify_otp.html', {
                'error': 'Please verify your email',
                'phone': phone
            })

        if not profile.is_admin_approved:
            return render(request, 'accounts/verify_otp.html', {
                'error': 'Waiting for admin approval',
                'phone': phone
            })

        login(request, user)
        return redirect('/')

    return redirect('send_otp')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
