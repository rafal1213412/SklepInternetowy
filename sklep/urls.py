from django.urls import path
from . import views

urlpatterns = [
    path("", views.sklep_home, name="sklep_home"),
]