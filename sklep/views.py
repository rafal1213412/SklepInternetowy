from django.shortcuts import render
from .models import Towar

def sklep_home(request):
    produkty = Towar.objects.all()
    return render(request, "home.html", {"produkty": produkty})