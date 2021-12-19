from typing import Counter
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,SetPasswordForm,PasswordChangeForm)
from django.forms.fields import ImageField

from .models import UserBase,GENDER

class DateInput(forms.DateInput):
    input_type='date'
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Enter Username',min_length=4,max_length=50,help_text='please Enter the fucking username')
    email = forms.EmailField(max_length=100,help_text='Required',error_messages={'required':'You need email address'})
    first_name = forms.CharField(label='First Name',max_length=25)
    last_name = forms.CharField(label='Last Name',max_length=25)
    phone_number = forms.CharField(label='Enter Your Phone Number',max_length=15)
    town_city = forms.CharField(label='Enter Your City',max_length=150)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email','phone_number','country','town_city','first_name','last_name')


    def clean_username(self):
        print("reached Username Validation")
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            print("Duplicate Username")
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            print("Unsupported password")
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            print("Duplicate Email")
            raise forms.ValidationError('Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Phone Number'})
        self.fields['town_city'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'City'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserEditForm(forms.ModelForm):

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'}))

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='First Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Last Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name', 'id': 'form-lastname'}))

    phone_number = forms.CharField(
        label='Phone Number', min_length=4, max_length=16, widget=forms.TextInput(
            attrs={'class': 'js-masked-input form-control', 'placeholder': '+(xxx)xxx-xx-xx', 'id':'form-phn'}))

    town_city = forms.CharField(
        label='Home City', min_length=4, max_length=30, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Home City', 'id': 'form-city'}))

    about = forms.CharField(
        label='About', min_length=4, max_length=500, widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'About yourself ...', 'id': 'form-about'}))
    gender = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=GENDER)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    # image = forms.ImageField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'file'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name','last_name','phone_number','town_city','about','image','date_of_birth','gender','country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley there is no matching email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

class PwdChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old password', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Old Password', 'id': 'form-oldpass'}))
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'id': 'form-new-pass2'}))
