from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new user. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating user. Includes all the fields on
    the user, but replaces the password field with admin"s
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CreatePasswordForm(forms.Form):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={"readonly": True, "required": False}))
    password1 = forms.CharField(label=_("Password"), min_length=4, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), min_length=4, widget=forms.PasswordInput)
    user_hash = forms.CharField(widget=forms.HiddenInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError(_("You must confirm your password"))
        if password1 != password2:
            raise forms.ValidationError(_("Your passwords do not match"))
        return password2
