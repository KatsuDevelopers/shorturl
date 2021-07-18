from django import forms
from .models import URL

class URLCreateForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ('original', 'alias',)
