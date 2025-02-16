from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md w-full'})
    )
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input rounded-md w-full'})
    )
    
    class Meta:
        model = Consultation
        fields = ['service', 'preferred_date', 'preferred_time', 'description']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select rounded-md w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea rounded-md w-full', 'rows': 4}),
        }
