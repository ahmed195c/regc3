# forms.py
from django import forms
from .models import FinesAccidents

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = FinesAccidents
        fields = ['text', 'image']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'style': 'width: 100%;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }
