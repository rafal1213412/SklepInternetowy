from django.shortcuts import render
from .models import Towar, Kategoria, Podkategoria
from django.shortcuts import get_object_or_404


def sklep_home(request):
    promocje = Towar.objects.filter(cena_promocyjna__isnull=False)
    kategorie = Kategoria.objects.all()   # ← DODANE!
    return render(request, "home.html", {
        "promocje": promocje,
        "kategorie": kategorie,           # ← DODANE!
    })



def produkty_kategoria(request, kategoria_id):
    kategoria = get_object_or_404(Kategoria, id=kategoria_id)
    podkategorie = kategoria.podkategorie.all()

    return render(request, "kategoria.html", {
        "kategoria": kategoria,
        "podkategorie": podkategorie
    })

def produkty_podkategoria(request, podkategoria_id):
    podkategoria = get_object_or_404(Podkategoria, id=podkategoria_id)
    produkty = Towar.objects.filter(podkategoria=podkategoria)

    return render(request, "podkategoria.html", {
        "podkategoria": podkategoria,
        "produkty": produkty
    })

from django.shortcuts import render, get_object_or_404
from .models import Podkategoria, Towar

def podkategoria_view(request, pk):
    podkategoria = get_object_or_404(Podkategoria, id=pk)
    produkty = Towar.objects.filter(podkategoria=podkategoria)

    # FILTROWANIE
    producent = request.GET.get("producent")
    cena_min = request.GET.get("cena_min")
    cena_max = request.GET.get("cena_max")
    sort = request.GET.get("sort")  # <-- NOWE

    if producent:
        produkty = produkty.filter(producent__icontains=producent)

    if cena_min:
        produkty = produkty.filter(cena_jednostkowa__gte=cena_min)

    if cena_max:
        produkty = produkty.filter(cena_jednostkowa__lte=cena_max)

    # SORTOWANIE
    if sort == "cena_asc":
        produkty = produkty.order_by("cena_jednostkowa")
    elif sort == "cena_desc":
        produkty = produkty.order_by("-cena_jednostkowa")

    return render(request, "podkategoria.html", {
        "podkategoria": podkategoria,
        "produkty": produkty,
    })
def produkt_szczegoly(request, produkt_id):
    produkt = get_object_or_404(Towar, id=produkt_id)
    return render(request, "produkt_szczegoly.html", {"produkt": produkt})