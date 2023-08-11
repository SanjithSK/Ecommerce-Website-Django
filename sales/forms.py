from django import forms


class VariationForm(forms.Form):
    variation = forms.ModelChoiceField(
        queryset=Variation.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
    )
    quantity = forms.IntegerField(initial=1, min_value=1)
