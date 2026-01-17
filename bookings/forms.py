from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):

    room_count = forms.IntegerField(
        min_value=1,
        widget=forms.Select(),
        label="Number of Rooms"
    )

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'room_count']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }
