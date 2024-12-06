# forms.py
from django import forms
from .models import FinesAccidents, RegistredCars, EmployesInfo

class UserProfileForm(forms.ModelForm):
    car = forms.ModelChoiceField(
        queryset=RegistredCars.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    employee = forms.ModelChoiceField(
        queryset=EmployesInfo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = FinesAccidents
        fields = ['car', 'employee', 'text', 'image']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'carnumber',
                'placeholder': 'Enter your name',
                'style': 'width: 100%;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if 'car_number' in self.data:
            self.fields['car'].queryset = RegistredCars.objects.filter(carNumber__icontains=self.data.get('car_number'))
        if 'employee_number' in self.data:
            self.fields['employee'].queryset = EmployesInfo.objects.filter(ceoNumber__icontains=self.data.get('employee_number'))