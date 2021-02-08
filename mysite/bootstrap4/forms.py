from django import forms

class RecInputForm(forms.Form):
    url = forms.CharField(label='Mountain Project URL', max_length=100)