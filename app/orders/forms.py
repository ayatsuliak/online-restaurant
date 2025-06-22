from datetime import timedelta

from django import forms
from django.utils import timezone

from menu.models import MenuItem

from .models import Order


class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    scheduled_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
        error_messages={
            'invalid': 'Please enter a valid date and time.'
        }
    )

    class Meta:
        model = Order
        fields = ['items', 'scheduled_time']

    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data.get('scheduled_time', None)

        if scheduled_time is None:
            raise forms.ValidationError(
                "Please select a valid delivery date and time."
            )

        if timezone.is_naive(scheduled_time):
            scheduled_time = timezone.make_aware(scheduled_time,
                                                 timezone.get_current_timezone())

        now = timezone.now()
        min_time = now + timedelta(minutes=30)

        if scheduled_time < min_time:
            raise forms.ValidationError(
                "Delivery must be scheduled at least 30 minutes from now."
            )

        return scheduled_time
