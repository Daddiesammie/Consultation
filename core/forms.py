from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input rounded-md w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form-input rounded-md w-full'}),
            'subject': forms.TextInput(attrs={'class': 'form-input rounded-md w-full'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea rounded-md w-full', 'rows': 4}),
        }
