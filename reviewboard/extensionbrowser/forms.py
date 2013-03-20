from django import forms


class SearchForm(forms.Form):
    """Search form for the extension browser."""
    query = forms.CharField(label="Keywords")
