from django import forms

from django.core.exceptions import ValidationError

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
    boulder_lower = forms.IntegerField(label="Lowest Boulder Grade: V", min_value=0, max_value=16, 
        initial=0)
    boulder_upper = forms.IntegerField(label="Highest Boulder Grade: V", min_value=0, max_value=16,
        initial=3)
    route_lower = forms.CharField(label="Lowest Route Grade: 5.", max_length=3, initial="8")
    route_upper = forms.CharField(label="Highest Route Grade: 5.", max_length=3, initial="10d")

    def clean(self):
        """
        This first runs default cleaning code (as defined by the field type and various parameters)
        then runs some custom cleaning code in order to verify:
        1. The boulder_lower is a lower or equal difficulty to the boulder_upper
        2. Both route_lower and route_upper contain valid difficulty strings
        3. The route_lower is a lower or equal difficulty to the route_upper 
        """
        # do the default form cleaning
        super().clean()

        # make sure that boulder_lower is lower or equal difficulty to boulder_upper
        bl = self.cleaned_data.get("boulder_lower")
        bu = self.cleaned_data.get("boulder_upper")
        if(bl > bu):
            raise ValidationError("Lower Boulder Grade should be less than or equal to Highest "
                "Boulder Grade")