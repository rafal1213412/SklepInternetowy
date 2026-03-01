from django.urls import path
from . import views

urlpatterns = [
    path("", views.sklep_home, name="sklep_home"),
    path("kategoria/<int:kategoria_id>/", views.produkty_kategoria, name="produkty_kategoria"),
    path("podkategoria/<int:pk>/", views.podkategoria_view, name="podkategoria_view"),
    path("produkt/<int:produkt_id>/", views.produkt_szczegoly, name="produkt_szczegoly"),
    path("search/", views.search, name="search"),
]