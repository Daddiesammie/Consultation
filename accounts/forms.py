from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input rounded-md w-full'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input rounded-md w-full'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company', 'phone', 'bio', 'profile_image']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-input rounded-md w-full'}),
            'phone': forms.TextInput(attrs={'class': 'form-input rounded-md w-full'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea rounded-md w-full', 'rows': 4}),
        }