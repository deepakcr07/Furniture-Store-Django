from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line', 'city', 'state', 'pincode', 'landmark', 'is_default']
        widgets = {
            'address_line': forms.Textarea(attrs={'rows': 3}),
            'landmark': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }