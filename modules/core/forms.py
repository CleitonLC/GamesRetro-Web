from django import forms
from modules.core.models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['console', 'game_rom']