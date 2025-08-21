from django import forms
import re

HANDLE_RE = re.compile(r'^[a-zA-Z0-9._-]{3,30}$')  # без @, 3–30 символов

class HandleForm(forms.Form):
    handle = forms.CharField(
        label='Псевдоним канала',
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'например: somechannel',
        })
    )

    def clean_handle(self):
        h = self.cleaned_data['handle'].strip()
        if not HANDLE_RE.match(h):
            raise forms.ValidationError('Допустимы латиница, цифры, точка, дефис, подчёркивание. Без @.')
        return h.lower()
