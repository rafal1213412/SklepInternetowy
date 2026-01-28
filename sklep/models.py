from django.db import models
from django.contrib.auth.models import User


class Klient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    email = models.EmailField()
    nr_tel = models.CharField(max_length=20)

    class Meta:
        db_table = "klienci"
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Konto(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    login = models.CharField(max_length=50)
    hash_hash = models.CharField(max_length=255)

    class Meta:
        db_table = "konta"
        verbose_name = "Konto"
        verbose_name_plural = "Konta"

    def __str__(self):
        return self.login


class Adres(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='adresy')
    miasto = models.CharField(max_length=100)
    ulica = models.CharField(max_length=100)
    kod_pocztowy = models.CharField(max_length=20)
    nr_domu = models.CharField(max_length=10)
    nr_mieszkania = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "adresy"
        verbose_name = "Adres"
        verbose_name_plural = "Adresy"

    def __str__(self):
        return f"{self.ulica} {self.nr_domu}, {self.miasto}"


class RodzajDostawy(models.Model):
    nazwa = models.CharField(max_length=50)

    class Meta:
        db_table = "rodzaje_dostawy"
        verbose_name = "Rodzaj dostawy"
        verbose_name_plural = "Rodzaje dostawy"

    def __str__(self):
        return self.nazwa


class Dostawa(models.Model):
    rodzaj = models.ForeignKey(RodzajDostawy, on_delete=models.PROTECT)
    cena_dostawy = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "dostawy"
        verbose_name = "Dostawa"
        verbose_name_plural = "Dostawy"

    def __str__(self):
        return f"{self.rodzaj.nazwa} ({self.cena_dostawy} zł)"


class Rabat(models.Model):
    nazwa = models.CharField(max_length=100)
    procent = models.DecimalField(max_digits=5, decimal_places=2)
    aktywny = models.BooleanField(default=True)

    class Meta:
        db_table = "rabaty"
        verbose_name = "Rabat"
        verbose_name_plural = "Rabaty"

    def __str__(self):
        return f"{self.nazwa} ({self.procent}%)"


class Pracownik(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    pesel = models.CharField(max_length=11)
    wynagrodzenie = models.DecimalField(max_digits=10, decimal_places=2)
    stanowisko = models.CharField(max_length=100)

    class Meta:
        db_table = "pracownicy"
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Kategoria(models.Model):
    nazwa_kategorii = models.CharField(max_length=50)

    class Meta:
        db_table = "kategorie"
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.nazwa_kategorii


class Towar(models.Model):
    nazwa = models.CharField(max_length=255)
    producent = models.CharField(max_length=100, blank=True, null=True)
    opis = models.TextField(blank=True, null=True)
    cena_jednostkowa = models.DecimalField(max_digits=10, decimal_places=2)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "towary"
        verbose_name = "Towar"
        verbose_name_plural = "Towary"

    def __str__(self):
        return self.nazwa


class Magazyn(models.Model):
    towar = models.ForeignKey(Towar, on_delete=models.CASCADE)
    ilosc_dostepna = models.IntegerField()

    class Meta:
        db_table = "magazyn"
        verbose_name = "Magazyn"
        verbose_name_plural = "Magazyn"

    def __str__(self):
        return f"{self.towar} ({self.ilosc_dostepna} szt.)"


class Zamowienie(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    adres = models.ForeignKey(Adres, on_delete=models.PROTECT)
    dostawa = models.ForeignKey(Dostawa, on_delete=models.PROTECT)
    pracownik = models.ForeignKey(Pracownik, on_delete=models.SET_NULL, null=True, blank=True)
    rabat = models.ForeignKey(Rabat, on_delete=models.SET_NULL, null=True, blank=True)
    data_zamowienia = models.DateTimeField()
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "zamowienia"
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

    def __str__(self):
        return f"Zamówienie {self.id}"


class PozycjaZamowienia(models.Model):
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.CASCADE, related_name='pozycje')
    towar = models.ForeignKey(Towar, on_delete=models.PROTECT)
    ilosc = models.IntegerField()
    cena_zakupu = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "pozycje_zamowienia"
        verbose_name = "Pozycja zamówienia"
        verbose_name_plural = "Pozycje zamówienia"

    def __str__(self):
        return f"{self.towar} x {self.ilosc}"


class StatusPlatnosci(models.Model):
    nazwa = models.CharField(max_length=50)

    class Meta:
        db_table = "statusy_platnosci"
        verbose_name = "Status płatności"
        verbose_name_plural = "Statusy płatności"

    def __str__(self):
        return self.nazwa


class Platnosc(models.Model):
    zamowienie = models.OneToOneField(Zamowienie, on_delete=models.CASCADE, related_name='platnosc')
    data_platnosci = models.DateTimeField()
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    metoda = models.CharField(max_length=100)
    status = models.ForeignKey(StatusPlatnosci, on_delete=models.PROTECT)

    class Meta:
        db_table = "platnosci"
        verbose_name = "Płatność"
        verbose_name_plural = "Płatności"

    def __str__(self):
        return f"Płatność za {self.zamowienie}"


class Atrybut(models.Model):
    nazwa = models.CharField(max_length=50)

    class Meta:
        db_table = "atrybuty"
        verbose_name = "Atrybut"
        verbose_name_plural = "Atrybuty"

    def __str__(self):
        return self.nazwa


class WartoscAtrybutu(models.Model):
    towar = models.ForeignKey(Towar, on_delete=models.CASCADE, related_name='wartosci_atrybutow')
    atrybut = models.ForeignKey(Atrybut, on_delete=models.CASCADE)
    wartosc = models.CharField(max_length=255)

    class Meta:
        db_table = "wartosci_atrybutow"
        verbose_name = "Wartość atrybutu"
        verbose_name_plural = "Wartości atrybutów"
        unique_together = ('towar', 'atrybut')

    def __str__(self):
        return f"{self.atrybut}: {self.wartosc}"


class Opinia(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    towar = models.ForeignKey(Towar, on_delete=models.CASCADE)
    ocena = models.SmallIntegerField()
    tresc = models.TextField()
    data_wystawienia = models.DateTimeField()

    class Meta:
        db_table = "opinie"
        verbose_name = "Opinia"
        verbose_name_plural = "Opinie"

    def __str__(self):
        return f"Opinia {self.klient} o {self.towar}"


class StatusReklamacji(models.Model):
    nazwa = models.CharField(max_length=50)

    class Meta:
        db_table = "statusy_reklamacji"
        verbose_name = "Status reklamacji"
        verbose_name_plural = "Statusy reklamacji"

    def __str__(self):
        return self.nazwa


class Reklamacja(models.Model):
    opis = models.TextField()
    data_zgloszenia = models.DateTimeField()
    status = models.ForeignKey(StatusReklamacji, on_delete=models.PROTECT)
    pozycja = models.ForeignKey(PozycjaZamowienia, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "reklamacje"
        verbose_name = "Reklamacja"
        verbose_name_plural = "Reklamacje"

    def __str__(self):
        return f"Reklamacja {self.id}"