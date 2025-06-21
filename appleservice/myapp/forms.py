from django import forms
from django.forms import inlineformset_factory
from .models import Usluga, Zlecenie, Lokacja, Czesc

ServiceFormSet = inlineformset_factory(
    Zlecenie,
    Usluga,
    fields=('service', 'price', 'done'),
    extra=1,
    can_delete=True
)

StorageFormSet = inlineformset_factory(
    Lokacja,
    Czesc,
    fields=('nazwa', 'nr_seryjny', 'ilosc'),
    extra=1,
    can_delete=True
)