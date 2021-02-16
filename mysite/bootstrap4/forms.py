from django import forms

class NoColon(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(NoColon, self).__init__(*args, **kwargs)

class RecInputForm(NoColon):
    url = forms.URLField(label="Mountain Project UR:L", max_length=100)
    latitude = forms.DecimalField(label="Latitude:", initial=33.8734)
    longitude = forms.DecimalField(label="Longitude:", initial=-115.9010)
    rec = forms.MultipleChoiceField(label="Recommenders:", choices=(
        ("top_pop", "Top Popular"),
        ("other", "Other Recommender")))
    boulder_lower = forms.IntegerField(label="Lowest Boulder Grade: V")
    boulder_upper = forms.IntegerField(label="Highest Boulder Grade: V")
    route_lower = forms.IntegerField(label="Lowest Route Grade: 5.")
    route_upper = forms.IntegerField(label="Highest Route Grade: 5.")