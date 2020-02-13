from django import forms
from django.contrib.auth.models import User
from mainApp.models import UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('__all__')
        exclude = ('user',)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
                'email',
                'first_name',
                'last_name',
                'password'
            )

# class ItemForm(forms.ModelForm):
#     longitude = forms.IntegerField(widget=forms.MapIn())

