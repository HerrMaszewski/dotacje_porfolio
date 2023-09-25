from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Hasło',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Powtórz hasło',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise ValidationError("Użytkownik z tym adresem email już istnieje.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.is_password_valid(password):
            raise ValidationError('Hasło musi zawierać co najmniej 8 znaków, dużą literę, małą literę, liczbę i znak specjalny.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Hasła nie są takie same.")

        return cleaned_data

    @staticmethod
    def is_password_valid(password):
        if len(password) < 8:
            return False

        # Checks for the password criteria
        if not re.search("[a-z]", password) or \
           not re.search("[A-Z]", password) or \
           not re.search("[0-9]", password) or \
           not re.search("[!@#$%^&*()_+=\[\]{};':\"\\|,.<>?~]", password):
            return False
        return True


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class DonationForm(forms.Form):
    quantity = forms.IntegerField()
    # categories = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                                     widget=forms.RadioSelect(attrs={}), empty_label=None)
    # institution = forms.ModelChoiceField(queryset=Institution.objects.all(), widget=forms.RadioSelect(attrs={}),
    #                                      empty_label=None)
    address = forms.CharField(max_length=128)
    phone_number = forms.IntegerField()
    city = forms.CharField(max_length=128)
    zip_code = forms.CharField(max_length=6)
    pick_up_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'RRRR-MM-DD'}))
    pick_up_time = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': '--:--'}))
    pick_up_comment = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}), required=False)


