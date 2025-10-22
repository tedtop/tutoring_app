from django import forms
from .models import TA, TutoringHour

class TASignupForm(forms.ModelForm):
    class Meta:
        model = TA
        fields = ['major', 'bio', 'courses']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'courses': forms.CheckboxSelectMultiple(),
        }

class TutoringHourForm(forms.ModelForm):
    class Meta:
        model = TutoringHour
        fields = ['day_of_week', 'start_time', 'end_time', 'is_recurring', 'until_date']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'until_date': forms.DateInput(attrs={'type': 'date'}),
        }
