# forms.py
from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label='Enter Your Search Term', max_length=100)
