from django import forms
from django.contrib.auth.models import User
from .models import Safaricom ,MShwari , Account

class CustomRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, label="Phone Number")  # Add phone number input
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    id_number = forms.CharField(max_length=20, label="ID Number")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'id_number', 'email', 'phone_number']  # Include phone_number

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        id_number = cleaned_data.get('id_number')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')

        # Check for password match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        # Validate against Safaricom records
        try:
            safaricom_user = Safaricom.objects.get(
                first_name=first_name,
                last_name=last_name,
                id_number=id_number
            )
            if safaricom_user.phone_number != phone_number:
                raise forms.ValidationError("Phone number does not match Safaricom records.")
        except Safaricom.DoesNotExist:
            raise forms.ValidationError("Details do not match Safaricom records.")
        
        return cleaned_data


class MShwariAccountForm(forms.ModelForm):
    class Meta:
        model = MShwari
        fields = ['available_balance', 'locked_balance']  # Do not include 'account' here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 'account' is not included as a field, so no need to modify the queryset here