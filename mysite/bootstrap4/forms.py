from django import forms

class RecInputForm(forms.Form):
    url = forms.URLField(label="Mountain Project URL", max_length=100)
    latitude = forms.DecimalField(label="Latitude")
    longitude = forms.DecimalField(label="Longitude")
    rec = forms.MultipleChoiceField(label="Recommenders", choices=(
        ("1", "Top Popular"),
        ("2", "Other Recommender")))