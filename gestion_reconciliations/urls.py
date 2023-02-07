from .import views
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


app_name = "reco_gest"

urlpatterns = [
    path('', views.dashboard,name="dashboard"),
    path('provinces', views.provinces,name="provinces"),
    path('villes', views.villes,name="villes"),
    path('type-magasin', views.type_magasin,name="type_magasin"),
    path('type-compte', views.type_compte,name="type_compte"),
    path('creer-magasin', views.creer_magasin,name="creer_magasin"),
    path('creer-compte', views.creer_compte,name="creer_compte"),
    path('details-compte', views.voir_details_compte,name="voir_details_compte"),
    path('liste-magasins', views.liste_magasin,name="liste_magasin"),
    path('recette-airtel', views.recette_airtel,name="recette_airtel"),
    path('recette-moov', views.recette_moov,name="recette_moov"),
    path('recuper-province', views.get_province,name="get_province"),
    path('recuper-ville', views.get_ville,name="get_ville"),
    path('edition/<int:id>/magasin', views.editer_magasin,name="editer_magasin"),
    path('recuper-type-magasin', views.get_typemagasin,name="get_typemagasin"),
    path('index2', views.index2,name="index2"),
    path('index4', views.index4,name="index4"),
    path('index5', views.index5,name="index5"),
    path('login', views.connexion,name="connexion"),
]