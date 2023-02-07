import json
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import ProvinceForm, TypeMagasinForm, MagasinForm, TypeCompteForm, CompteForm, VilleForm
from .models import Province, Ville, TypeMagasin, Magasin, TypeCompte, ExtendedEncoder
from django.forms import model_to_dict

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def dashboard(request):
    return render(request,"reconciliation/dashboard.html")

def provinces(request):
    provinces = Province.objects.all()
    act = "Enregistrer"
    if request.method == "GET":
        form = ProvinceForm()
    elif request.method == "POST":
        form = ProvinceForm(request.POST)
        if form.is_valid():
            if request.POST["idprovince"] == "":
                Province.objects.create(code=form.cleaned_data["codeprovince"],nom=form.cleaned_data["nomprovince"])
                messages.add_message(request, messages.INFO, 'Province enregistrée avec succès !')
            else:
                province = get_object_or_404(Province,pk=request.POST["idprovince"])
                province.code = form.cleaned_data["codeprovince"]
                province.nom = form.cleaned_data["nomprovince"]
                province.save()
                messages.add_message(request, messages.INFO, 'Province modifiée" avec succès !')
        else:
            if request.POST["idprovince"] != "":
                act = "Editer"
    return render(request,"reconciliation/provinces.html",{"form":form,"provinces":provinces,"act":act})

def get_province(request):
    if is_ajax(request=request) and request.method=="POST":
        province = Province.objects.get(id=request.POST["id_province"])
        province = model_to_dict(province)
        province = json.dumps(province)
        mimetype = "application/json"
        return HttpResponse(province, mimetype)
    else:
        return HttpResponse("Erreur")

def get_ville(request):
    if is_ajax(request=request) and request.method=="POST":
        ville = Ville.objects.get(id=request.POST["id_ville"])
        ville = model_to_dict(ville)
        ville = json.dumps(ville)
        mimetype = "application/json"
        return HttpResponse(ville, mimetype)
    else:
        return HttpResponse("Erreur")

def get_typemagasin(request):
    if is_ajax(request=request) and request.method=="POST":
        typemagasin = TypeMagasin.objects.get(id=request.POST["id_typemag"])
        typemagasin = model_to_dict(typemagasin)
        typemagasin = json.dumps(typemagasin,cls=ExtendedEncoder)
        mimetype = "application/json"
        return HttpResponse(typemagasin, mimetype)
    else:
        return HttpResponse("Erreur")

def villes(request):
    villes = Ville.objects.all()
    act = "Enregistrer"
    if request.method == "GET":
        form = VilleForm()
    elif request.method == "POST":
        form = VilleForm(request.POST)
        if form.is_valid():
            province = form.cleaned_data["provinces"]
            if request.POST["idville"] == "":
                Ville.objects.create(province=province,nom_ville=form.cleaned_data["nomville"])
                messages.add_message(request, messages.INFO, 'Ville enregistrée" avec succès !')
            else:
                ville = get_object_or_404(Ville,pk=request.POST["idville"])
                ville.province = province
                ville.nom_ville = form.cleaned_data["nomville"]
                ville.save()
                messages.add_message(request, messages.INFO, 'Ville modifiée" avec succès !')
        else:
            if request.POST["idville"] != "":
                act = "Editer"
    return render(request,"reconciliation/villes.html",{"villes":villes,"form":form,"act":act})



def type_magasin(request):
    t_magasins = TypeMagasin.objects.all()
    act = "Enregistrer"
    if request.method == "GET":
        form = TypeMagasinForm()
    elif request.method == "POST":
        form = TypeMagasinForm(request.POST)
        if form.is_valid():
            if request.POST["idtypemagasin"] == "":
                TypeMagasin.objects.create(code_type=form.cleaned_data["code"],libelle=form.cleaned_data["libelle"])
                messages.add_message(request, messages.INFO, 'Type de magasin enregistré avec succès !')
            else:
                typemagasin = get_object_or_404(TypeMagasin,pk=request.POST["idtypemagasin"])
                typemagasin.code_type = form.cleaned_data["code"]
                typemagasin.libelle = form.cleaned_data["libelle"]
                typemagasin.save()
                messages.add_message(request, messages.INFO, 'Type de magasin modifié avec succès !')
        else:
            if request.POST["idtypemagasin"] != "":
                act = "Editer"
    return render(request,"reconciliation/type_magasin.html",{"form":form,"t_magasins":t_magasins,"act":act})

def type_compte(request):
    t_comptes = TypeCompte.objects.all()
    if request.method == "GET":
        form = TypeCompteForm()
    elif request.method == "POST":
        form = TypeCompteForm(request.POST)
        if form.is_valid():
            TypeCompte.objects.create(code=form.cleaned_data["code"],libelle=form.cleaned_data["libelle"])
    return render(request,"reconciliation/type_compte.html",{"form":form,"t_comptes":t_comptes})

def creer_magasin(request):
    form = MagasinForm()
    if request.method == "POST":
        form = MagasinForm(request.POST)
        if form.is_valid():
            ville = form.cleaned_data["ville"]
            type_magasin = form.cleaned_data["type_magasin"]
            Magasin.objects.create(
                adresse=form.cleaned_data["adresse"], commune=form.cleaned_data["commune"],
                ville=ville,type_magasin=type_magasin,nom_magasin=form.cleaned_data["nom_magasin"],
                point_repere=form.cleaned_data["point_repere"],telephone=form.cleaned_data["telephone"],
                latitude=form.cleaned_data["latitude"],longitude=form.cleaned_data["longitude"],
                email=form.cleaned_data["email"]
            )
            messages.add_message(request,messages.INFO,"Magasin enregistré avec succès")
            return render(request,"reconciliation/liste_magasin.html")
    return render(request,"reconciliation/creer_magasin.html",{"form":form})


def liste_magasin(request):
    context = {
        "villes": Ville.objects.all(),
        "magasins": Magasin.objects.all(),
        "provinces": Province.objects.all()
    }
    liste = {}
    for province in Province.objects.all():
        nb_magasins = Magasin.objects.filter(ville__province__nom=province.nom).count()
        liste[province.nom] = nb_magasins
    context["liste"] = liste
    return render(request,"reconciliation/liste_magasin.html",context)

def editer_magasin(request,id):
    magasin = Magasin.objects.get(pk=id)
    initial = {
        "type_magasin":magasin.type_magasin,"ville":magasin.ville,"nom_magasin":magasin.nom_magasin,
        "adresse":magasin.adresse,"commune":magasin.commune,"point_repere":magasin.point_repere,
        "telephone":magasin.telephone,"latitude":magasin.latitude,"longitude":magasin.longitude,
        "email":magasin.email
    }
    form = MagasinForm(initial=initial)
    if request.method == "POST":
        if form.is_valid():
            magasin.type_magasin = form.cleaned_data["type_magasin"]
            magasin.ville = form.cleaned_data["ville"]
            magasin.nom_magasin = form.cleaned_data["nom_magasin"]
            magasin.adresse = form.cleaned_data["adresse"]
            magasin.commune = form.cleaned_data["commune"]
            magasin.point_repere = form.cleaned_data["point_repere"]
            magasin.latitude = form.cleaned_data["latitude"]
            magasin.longitude = form.cleaned_data["longitude"]
            magasin.email = form.cleaned_data["email"]
            magasin.telephone = form.cleaned_data["telephone"]
            magasin.save()
            return render(request, "reconciliation/liste_magsin.html")
        else:
            print("ooooooooe")
            print(form.errors)
            print("ooooooooe")
    return render(request,"reconciliation/editer_magasin.html",{"form":form})

def creer_compte(request):
    context = {
        "magasins": Magasin.objects.all(),
        "t_comptes": TypeMagasin.objects.all()
    }
    if request.method == "GET":
        context["form"] = CompteForm()
    elif request.method == "POST":
        context["form"] = CompteForm(request.POST)
    return render(request,"reconciliation/creer_compte.html",context)

def recette_airtel(request):
    return render(request,"reconciliation/recette_airtel.html")

def recette_moov(request):
    return render(request,"reconciliation/recette_airtel.html")

def voir_details_compte(request):
    return render(request,"reconciliation/details_compte.html")
def index2(request):
    return render(request,"reconciliation/formlayouts.html")

def index4(request):
    return render(request,"reconciliation/widgets.html")

def index5(request):
    return render(request,"reconciliation/widgets.html")

def connexion(request):
    return render(request,"reconciliation/login.html")


# Create your views here.
