from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import Profile


class CustomAuthenticationForm(AuthenticationForm):
    # def __init__(self, *args, **kwargs):
    #     super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs.update({"class": "form-control"})
    #         if self.errors.get(field_name):
    #             field.widget.attrs["class"] += " is-invalid"

    remember_me = forms.BooleanField(required=False, initial=True)


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
            if field_name == "agree_terms":
                field.widget.attrs.update({"class": "form-check-input me-2"})
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

    agree_terms = forms.BooleanField(
        required=True,
        initial=False,
        label="I agree all statements in ",
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["gender", "date_of_birth", ]
        widgets = {
            "date_of_birth": forms.DateInput(
                format="%m/%d/%Y", attrs={"type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control form-control-lg"}
            )
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"
