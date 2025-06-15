from django import forms
from django.forms import inlineformset_factory
from .models import Usluga, Zlecenie

ServiceFormSet = inlineformset_factory(
    Zlecenie,
    Usluga,
    fields=('service', 'price', 'done'),
    extra=1,
    can_delete=True
)