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
