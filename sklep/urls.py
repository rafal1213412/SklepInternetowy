from django.urls import path
from . import views

urlpatterns = [
    path("", views.sklep_home, name="sklep_home"),
    path("kategoria/<int:kategoria_id>/", views.produkty_kategoria, name="produkty_kategoria"),
    path("podkategoria/<int:podkategoria_id>/", views.produkty_podkategoria, name="produkty_podkategoria"),
]