from django.contrib import admin
from .models import (
    Klient,
    Konto,
    Adres,
    RodzajDostawy,
    Dostawa,
    Rabat,
    Pracownik,
    Kategoria,
    Towar,
    Magazyn,
    Zamowienie,
    PozycjaZamowienia,
    StatusPlatnosci,
    Platnosc,
    Atrybut,
    WartoscAtrybutu,
    Opinia,
    StatusReklamacji,
    Reklamacja,
    Podkategoria

)
MODELE = [
    Klient,
    Konto,
    Adres,
    RodzajDostawy,
    Dostawa,
    Rabat,
    Pracownik,
    Kategoria,
    Towar,
    Magazyn,
  #  Zamowienie,
    PozycjaZamowienia,
    StatusPlatnosci,
    Platnosc,
    Atrybut,
    WartoscAtrybutu,
    Opinia,
    StatusReklamacji,
    Reklamacja,
    Podkategoria,
]

for model in MODELE:
    admin.site.register(model)