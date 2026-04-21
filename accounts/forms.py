from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class StudentRegistrationForm(UserCreationForm):
    """Registration form for students."""
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user


class InstructorRegistrationForm(UserCreationForm):
    """Registration form for instructors."""
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'instructor'
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    """Custom login form with styled fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password',
        })


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information."""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio', 'phone', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'profile_image':
                field.widget.attrs['class'] = 'form-input'
            else:
                field.widget.attrs['class'] = 'form-file-input'
