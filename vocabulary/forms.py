from django import forms


class WordSearchForm(forms.Form):
    text = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search word or phrase"
            }
        )
    )


class WordListSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by list title"
            }
        )
    )
