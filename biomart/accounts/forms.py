from django import forms
from django.forms import SelectDateWidget
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from .models import Buyer, Seller
from django.utils import timezone


def past_years(ago):
    this_year = timezone.now().year
    return list(range(this_year-ago-1, this_year))

class BuyerRegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    dob = forms.DateField(widget=SelectDateWidget(years=past_years(80)))
    email = forms.EmailField()
    phone = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')       
        if password1 != password2 and password1 is not None:
            self.add_error('password', 'Your passwords do not match')
            

    def clean_username(self):
        temp_username = self.cleaned_data.get('username')
        temp = User.objects.filter(username=temp_username)
        if temp.exists():
            raise forms.ValidationError('Username already taken')
        return temp_username

    def clean_phone(self):
        temp_phone = self.cleaned_data.get('phone')
        if not temp_phone.isnumeric():
            raise forms.ValidationError('Invalid Phone Number')
        return temp_phone


class SellerRegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    dob = forms.DateField()
    email = forms.EmailField()
    phone = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')       
        if password1 != password2 and password1 is not None:
            self.add_error('password', 'Your passwords do not match')
            

    def clean_username(self):
        temp_username = self.cleaned_data.get('username')
        temp = User.objects.filter(username=temp_username)
        if temp.exists():
            raise forms.ValidationError('Username already taken')
        return temp_username

