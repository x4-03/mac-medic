from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Lokacja(models.Model):
    nazwa_lokacji = models.CharField(max_length=16, primary_key=True)
    miasto = models.CharField(max_length=32)
    adres = models.CharField(max_length=32)
    kod_pocztowy = models.CharField(max_length=6)

class Klient(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    imie = models.CharField(max_length=64)
    nazwisko = models.CharField(max_length=64)
    email = models.CharField(max_length=64, unique=True)
    haslo = models.CharField(max_length=256)
    telefon = models.CharField(max_length=9, blank=True, default='')
    firma = models.CharField(max_length=64, blank=True, default='')
    nip = models.CharField(max_length=15, blank=True, default='')
    adres = models.CharField(max_length=64, blank=True, default='')
    miasto = models.CharField(max_length=64, blank=True, default='')
    kod_pocztowy = models.CharField(max_length=6, blank=True, default='')

class Pracownik(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    imie = models.CharField(max_length=64)
    nazwisko = models.CharField(max_length=64)
    email = models.CharField(max_length=64, unique=True)
    haslo = models.CharField(max_length=256)
    telefon = models.CharField(max_length=9)
    lokacja = models.ForeignKey(Lokacja, on_delete = models.CASCADE)
    zatwierdzony = models.BooleanField(default=False)

def validate_time(value):
    if value.weekday() in [5, 6]:  #0-6 pon-nd
        raise ValidationError("Wizyty tylko od poniedziałku do piątku!")

    if not (8 <= value.hour < 16):
        raise ValidationError("Wizyta musi być między 8:00 a 16:00!")
    
    # Check for 10-minute intervals
    if value.minute % 10 != 0:
        raise ValidationError("Terminy wizyt są tylko co 10 minut!")

class Zlecenie(models.Model):
    id_zlecenia = models.CharField(max_length=32, primary_key=True)
    id_klienta = models.ForeignKey(Klient, on_delete=models.CASCADE)
    id_lokacji = models.ForeignKey(Lokacja, on_delete=models.CASCADE, default=None)
    id_pracownika = models.ForeignKey(Pracownik, on_delete=models.CASCADE, blank=True, null=True, default=None)
    class Status(models.IntegerChoices):
        OCZEKIWANIE = 0, "Oczekiwanie" # od wysłania zlecenia przez klienta do wizyty w salonie
        W_REALIZACJI = 1, "W realizacji" # od wizyty do zakończenia napraw itd.
        ZREALIZOWANO = 2, "Zrealizowano" # klient przychodzi po odbiór w godzinach otwarcia salonu, dostaje fakture/paragon
        ZARCHIWIZOWANO = 3, "Zarchiwizowano" # urządzenie odebrano; zlecenie wciąż widoczne, zawsze można usunąć z bazy ale po co
    status_zlecenia = models.IntegerField(choices=Status, default=0)
    termin_zlecenia = models.DateTimeField(validators=[validate_time]) # termin w którym klient przyjdzie na wizyte
    termin_realizacji = models.DateTimeField(blank=True, null=True) #termin zakończenia prac, nie odbioru. zapisanie terminu odbioru jest nieistotne, po archiwizacji będzie widać że urządzenie odebrano
    model = models.CharField(max_length=32)
    nr_seryjny = models.CharField(max_length=32, blank=True, null=True)
    pakiet_diagnostyczny = models.BooleanField(default=False)
    diagonza = models.TextField(default=". . .", blank=True, null=True)
    notes = models.TextField(default=". . .", blank=True, null=True)

class Usluga(models.Model):
    order = models.ForeignKey(Zlecenie, on_delete=models.CASCADE, related_name='usluga')
    service = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service} (Zlecenie #{self.order.id_zlecenia})"
