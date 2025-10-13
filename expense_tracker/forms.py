from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your username", "class": "form-control"}
        ),
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            {"placeholder": "Enter your password", "class": "form-control"}
        ),
        required=True,
    )

# 
# class RegistrationForm(form)