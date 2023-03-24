import json

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from .forms import ProvinceForm, TypeMagasinForm, MagasinForm, TypeCompteForm, CompteForm, VilleForm, UserForm,LoginForm
from .models import Province, Ville, TypeMagasin, Magasin, TypeCompte, ExtendedEncoder, CompteMarchand, Utilisateur, \
    Roles, Affectation
from django.forms import model_to_dict

def module(request,module):
    request.session["module"] = module

@login_required(login_url='/connexion')
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def reporting(request):
    module(request,"reporting")
    return render(request,"reporting/reporting.html")

def choisir_module(request):
    return render(request,"reconciliation/choix_module.html")
@login_required(login_url='/connexion')
def dashboard_recette(request):
    module(request,"recette")
    # import requests
    # headers = {
    #     'Content-Type': 'application/json',
    #     'Accept': '*/*'
    # }
    # data = {
    #     "client_id": "8a151941-2350-4d3c-9377-12ec86fd3d19",
    #     "client_secret": "456416",
    #     "grant_type": "client_credentials"
    # }
    # data = json.dumps(data)
    # r = requests.post('https://openapiuat.airtel.africa/auth/oauth2/token', headers=headers,data=data)
    # print(r.json())
    context = {}
    context["recettes_par_prov"] = Province.objects.all()
    return render(request,"recette/dashboard.html",context)

def detail_type_mag(request,libelle_typemag):
    module(request, "recette")
    liste_mags = []
    mags = {}
    mags_queryset = TypeMagasin.objects.select_related("magasins").values("magasins__ville__nom_ville","libelle").filter(libelle=libelle_typemag)
    for mag in mags_queryset:
        ville = mag["magasins__ville__nom_ville"]
        mags[ville] = mag["libelle"]
    liste_mags.append(mags)
    print(mags)
    return render(request,"recette/detail_type_mag.html",{"mags":mags,"libelle_typemag":libelle_typemag,"liste_mags":liste_mags})
@login_required(login_url='/connexion')
def liste_utilisateurs(request):
    module(request, "users")
    Utilisateur.objects.filter(id=2).update(telephone="066638018")
    users = Utilisateur.objects.all()
    return render(request,"utilisateurs/liste_utilisateurs.html",{"users":users})
@login_required(login_url='/connexion')
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        if user.is_active == False:
            user.is_active = True
        return render(request, "reconciliation/bienvenue.html")
    else:
        return HttpResponse("Lien d'activation invalide.")

def dashboard_user(request):
    module(request, "users")
    users_connectes = Utilisateur.objects.filter(user__is_active=True)
    return render(request,"utilisateurs/dashboard_users.html",{"users_connects":users_connectes})
@login_required(login_url='/connexion')
def creer_user(request):
    module(request, "users")
    form = UserForm()
    villes = Ville.objects.all()
    if request.method == "POST":
        form = UserForm(request.POST)
        if request.POST["ville"] == "":
            messages.add_message(request, messages.WARNING, 'Veillez selectionner une ville pour continuer')
        else:
            if form.is_valid():
                password = User.objects.make_random_password()
                if User.objects.filter(email=form.cleaned_data["email"]) or User.objects.filter(username=form.cleaned_data["nom"]):
                    messages.add_message(request,messages.WARNING,"Nom ou email déja enregistré")
                else:
                    ville = get_object_or_404(Ville,pk=request.POST["ville"])
                    user = User(email=form.cleaned_data["email"],username=form.cleaned_data["nom"])
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    roles = Roles.objects.create(
                        admin=form.cleaned_data["admin"], visiteur=form.cleaned_data["operateur"],
                    )
                    try:
                        user.first_name = form.cleaned_data["prenom"]
                        user.last_name = form.cleaned_data["nom"]
                        user.save()
                        utilisateur = Utilisateur(
                            adresse=form.cleaned_data["adresse"], telephone=form.cleaned_data["telephone"],
                            ville=ville,roles=roles,user=user,
                        )
                        utilisateur.save()
                        # Affectation.objects.create(
                        #     Utilisateur=utilisateur,magasin=magasin
                        # )
                    except Exception as e:
                        print(e)
                        user.delete()
                        roles.delete()
                    message = render_to_string("reconciliation/activate_email.html",
                                               {"user": user, "domaine": request.META['HTTP_HOST'],
                                                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                                                "token": default_token_generator.make_token(user), "password": password})
                    email_to_send = EmailMessage("Activation du compte", message, to=[form.cleaned_data["email"]])
                    email_to_send.send(fail_silently=False)
                    messages.add_message(request, messages.INFO,"Un méssage a été envoyé é l'adresse %s pour confirmation" % form.cleaned_data["email"])
                    return render(request,"utilisateurs/dashboard_users.html",{"form":form,"villes":villes})
            else:
                print(form.errors)
                return render(request,"utilisateurs/nouveau_user.html",{"form":form,"villes":villes})
    else:
        render(request,"utilisateurs/nouveau_user.html",{"form":form,"villes":villes})
    return render(request,"utilisateurs/nouveau_user.html",{"villes":villes,"form":form})

def editer_utilisateur(request,id):
    module(request, "users")
    utilisateur = get_object_or_404(Utilisateur,pk=id)
    initial = {
        "nom":utilisateur.user.last_name,"prenom":utilisateur.user.first_name,
        "adresse":utilisateur.adresse,"telephone":utilisateur.telephone,
        "email":utilisateur.user.email
    }
    villes = Ville.objects.all()
    form = UserForm(initial=initial)
    return render(request,"utilisateurs/editer_user.html",{"villes":villes,"utilisateur":utilisateur,"form":form})
@login_required(login_url='/connexion')
def provinces(request):
    module(request, "users")
    provinces = Province.objects.all()
    act = "Enregistrer"
    if request.method == "GET":
        form = ProvinceForm()
    elif request.method == "POST":
        if request.POST["idprovince"] == "":
            form = ProvinceForm(request.POST)
            if form.is_valid():
                Province.objects.create(code=form.cleaned_data["codeprovince"],nom=form.cleaned_data["nomprovince"])
                messages.add_message(request, messages.INFO, 'Province enregistrée avec succès !')
        else:
            instance = get_object_or_404(Province,pk=request.POST["idprovince"])
            form = ProvinceForm(request.POST,instance=instance)
            form.save()
            act = "Enregistrer"
            messages.add_message(request, messages.INFO, 'Province modifiée" avec succès !')
    return render(request,"utilisateurs/provinces.html",{"form":form,"provinces":provinces,"act":act})
@login_required(login_url='/connexion')
def get_province(request):
    module(request, "users")
    if is_ajax(request=request) and request.method=="POST":
        province = Province.objects.get(id=request.POST["id_province"])
        province = model_to_dict(province)
        province = json.dumps(province)
        mimetype = "application/json"
        return HttpResponse(province, mimetype)
    else:
        return HttpResponse("Erreur")

@login_required(login_url='/connexion')
def supprimer_operateur(request):
    module(request, "recette")
    reponse = {}
    if is_ajax(request=request) and request.method=="POST":
        operateur = get_object_or_404(TypeCompte,pk=request.POST["id_op"])
        if CompteMarchand.objects.filter(type_compte=operateur).exists():
            reponse["statut"] = "echec"
            reponse["message"] = "Impossible de supprimer un opérateur associé à un compte marchand"
        else:
            operateur.delete()
            reponse["statut"] = "succes"
            reponse["message"] = "Opérateur supprimé avec succès"
        reponse = json.dumps(reponse)
        mimetype = "application/json"
        return HttpResponse(reponse, mimetype)
    else:
        return HttpResponse("Erreur")

@login_required(login_url='/connexion')
def desactiver_user(request):
    module(request, "users")
    reponse = {}
    if is_ajax(request=request) and request.method=="POST":
        user = get_object_or_404(User,pk=request.POST["id_user"])
        if user.is_active:
            user.is_active = False
            user.save()
            reponse["statut"] = "succes"
            reponse["message"] = "Utilisateur désactivé"
        else:
            reponse["statut"] = "echec"
            reponse["message"] = "Cet utilisateur est déjà désactivé"
        reponse = json.dumps(reponse)
        mimetype = "application/json"
        return HttpResponse(reponse, mimetype)
    else:
        return HttpResponse("Erreur")
@login_required(login_url='/connexion')
def get_ville(request):
    module(request, "users")
    if is_ajax(request=request) and request.method=="POST":
        ville = Ville.objects.get(id=request.POST["id_ville"])
        ville = model_to_dict(ville)
        ville = json.dumps(ville)
        mimetype = "application/json"
        return HttpResponse(ville, mimetype)
    else:
        return HttpResponse("Erreur")
@login_required(login_url='/connexion')
def get_typemagasin(request):
    module(request, "recette")
    if is_ajax(request=request) and request.method=="POST":
        typemagasin = TypeMagasin.objects.get(id=request.POST["id_typemag"])
        typemagasin = model_to_dict(typemagasin)
        typemagasin = json.dumps(typemagasin,cls=ExtendedEncoder)
        mimetype = "application/json"
        return HttpResponse(typemagasin, mimetype)
    else:
        return HttpResponse("Erreur")
@login_required(login_url='/connexion')
def get_type_compte(request):
    module(request, "recette")
    if is_ajax(request=request) and request.method=="POST":
        typecompte = TypeCompte.objects.get(id=request.POST["idtypecompte"])
        typecompte = model_to_dict(typecompte)
        typecompte = json.dumps(typecompte)
        mimetype = "application/json"
        return HttpResponse(typecompte, mimetype)
    else:
        return HttpResponse("Erreur")
@login_required(login_url='/connexion')
def type_mag_dune_ville(request):
    module(request, "recette")
    if is_ajax(request=request) and request.method == "POST":
        ville = Ville.objects.get(id=request.POST["id_ville"])
        liste_type_mags = []
        for t in TypeMagasin.objects.filter(magasins__ville__nom_ville=ville.nom_ville):
            typemag = {"id":t.id,"libelle":t.libelle}
            liste_type_mags.append(typemag)
        typemags = json.dumps(liste_type_mags)
        mimetype = "application/json"
        return HttpResponse(typemags, mimetype)
    else:
        return HttpResponse("Erreur")
@login_required(login_url='/connexion')
def magasins_dun_type(request):
    module(request, "recette")
    if is_ajax(request=request) and request.method == "POST":
        typemag = TypeMagasin.objects.get(id=request.POST["typeid"])
        liste_mags = []
        for mag in Magasin.objects.filter(type_magasin__id=typemag.id):
            magasin = {"id":mag.id,"nom_magasin":mag.nom_magasin}
            liste_mags.append(magasin)
        magasins = json.dumps(liste_mags)
        mimetype = "application/json"
        return HttpResponse(magasins, mimetype)
    else:
        return HttpResponse("Erreur")

@login_required(login_url='/connexion')
def villes(request):
    module(request, "users")
    villes = Ville.objects.all()
    act = "Enregistrer"
    if request.method == "GET":
        form = VilleForm()
    elif request.method == "POST":
        if request.POST["idville"] == "":
            form = VilleForm(request.POST)
            if form.is_valid():
                province = form.cleaned_data["province"]
                Ville.objects.create(province=province,nom_ville=form.cleaned_data["nom_ville"])
                messages.add_message(request, messages.INFO, 'Ville enregistrée" avec succès !')
        else:
            ville = get_object_or_404(Ville,pk=request.POST["idville"])
            form = VilleForm(request.POST,instance=ville)
            form.save()
            act = "Enregistrer"
            messages.add_message(request, messages.INFO, 'Ville modifiée" avec succès !')
    return render(request,"utilisateurs/villes.html",{"villes":villes,"form":form,"act":act})
@login_required(login_url='/connexion')
def type_magasin(request):
    module(request, "recette")
    t_magasins = TypeMagasin.objects.all()
    act = "Enregistrer"
    if request.method == "GET":
        form = TypeMagasinForm()
    elif request.method == "POST":
        if request.POST["idtypemagasin"] == "":
            form = TypeMagasinForm(request.POST)
            if form.is_valid():
                TypeMagasin.objects.create(code_type=form.cleaned_data["code"],libelle=form.cleaned_data["libelle"])
                messages.add_message(request, messages.INFO, 'Type de magasin enregistré avec succès !')
        else:
            instance = get_object_or_404(TypeMagasin,pk=request.POST["idtypemagasin"])
            form = TypeMagasinForm(request.POST,instance=instance)
            if form.is_valid():
                form.save()
            act = "Enregistrer"
            messages.add_message(request, messages.INFO, 'Type de magasin modifié avec succès !')
    return render(request,"recette/type_magasin.html",{"form":form,"t_magasins":t_magasins,"act":act})
@login_required(login_url='/connexion')
def type_compte(request):
    module(request, "recette")
    t_comptes = TypeCompte.objects.all()
    act = "Enregistrer"
    if request.method == "GET":
        form = TypeCompteForm()
    elif request.method == "POST":
        form = TypeCompteForm(request.POST)
        if form.is_valid():
            if request.POST["idtypecompte"]=="":
                TypeCompte.objects.create(code=form.cleaned_data["code"],libelle=form.cleaned_data["libelle"])
                messages.add_message(request, messages.INFO, 'Type de compte enregistré avec succès !')
            else:
                type_compte = get_object_or_404(TypeCompte,pk=request.POST["idtypecompte"])
                type_compte.code = form.cleaned_data["code"]
                type_compte.libelle = form.cleaned_data["libelle"]
                type_compte.save()
                messages.add_message(request, messages.INFO, 'Type de compte modifié avec succès !')
        else:
            if request.POST["idtypecompte"] == "":
                act = "Editer"
    return render(request,"recette/type_compte.html",{"form":form,"t_comptes":t_comptes,"act":act})
@login_required(login_url='/connexion')
def creer_magasin(request):
    module(request, "recette")
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
    return render(request,"recette/creer_magasin.html",{"form":form})
@login_required(login_url='/connexion')
def magasin_par_province(request,nomtypemag):
    module(request, "recette")
    context = {"nb_total":TypeMagasin.objects.filter(libelle=nomtypemag).count(),"nomtypemag":nomtypemag}
    province = "magasins__ville__province__nom"
    ville = "magasins__ville__nom_ville"
    nb_t_mag = TypeMagasin.objects.values(province,ville).annotate(nb_prov=Count("magasins__ville__province")).filter(libelle=nomtypemag)
    context["nb_t_mag"] = nb_t_mag
    print(context["nb_t_mag"])
    return render(request,"recette/mag_par_province.html",context)
@login_required(login_url='/connexion')
def magasin_par_ville(request,nomtypemag,ville):
    module(request, "recette")
    v = "magasins__ville__nom_ville"
    context = {
        "nomtypemag":nomtypemag,
        "total_typemag": TypeMagasin.objects.filter(libelle=nomtypemag,magasins__ville__nom_ville=ville).count(),
        "nb_villes": Ville.objects.filter(mags__type_magasin__libelle=nomtypemag).count(),
        "nb_type_mag":TypeMagasin.objects.values(v).annotate(nb_ville=Count("magasins__ville")).filter(libelle=nomtypemag)
    }
    print(context["nb_type_mag"])
    return render(request,"recette/mag_par_ville.html",context)
@login_required(login_url='/connexion')
def liste_magasin(request):
    module(request, "recette")
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
    return render(request,"recette/liste_magasin.html",context)
@login_required(login_url='/connexion')
def editer_magasin(request,id):
    module(request, "recette")
    magasin = Magasin.objects.get(pk=id)
    form = MagasinForm(instance=magasin)
    if request.method == "POST":
        form = MagasinForm(request.POST, instance=magasin)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return render(request,"reconciliation/liste_magasin.html")
    return render(request,"recette/editer_magasin.html",{"form":form})
@login_required(login_url='/connexion')
def creer_compte(request):
    module(request, "recette")
    context = {
        "magasins": Magasin.objects.all(),
        "t_comptes": TypeMagasin.objects.all()
    }
    if request.method == "GET":
        context["compteform"] = CompteForm()
    elif request.method == "POST":
        compteform = CompteForm(request.POST)
        context["compteform"] = compteform
        if compteform.is_valid():
            magasin = compteform.cleaned_data["magasins"]
            typecompte = compteform.cleaned_data["typecompte"]
            CompteMarchand.objects.create(
                magasin=magasin,type_compte=typecompte,
                libelle_compte=compteform.cleaned_data["libelle"],
                numero_telephone=compteform.cleaned_data["numero"]
            )
            messages.add_message(request,messages.INFO,"Compte marchand crée avec succès")
    return render(request,"recette/creer_compte.html",context)

def recuperer_infos_compte(request):
    if is_ajax(request=request) and request.method == "POST":
        compte = CompteMarchand.objects.get(id=request.POST["id_compte"])
        compte = model_to_dict(compte)
        compte = json.dumps(compte)
        mimetype = "application/json"
        return HttpResponse(compte, mimetype)

def editer_compte(request):
    reponse = {}
    if is_ajax(request=request) and request.method == "POST":
        try:
            compte = CompteMarchand.objects.get(id=request.POST["id_compte"])
            compte.magasin = Magasin.objects.get(id=request.POST["id_mag"])
            compte.type_compte = TypeCompte.objects.get(id=request.POST["id_type"])
            compte.libelle = request.POST["code_client"]
            compte.numero_telephone = request.POST["num_tel"]
            compte.save()
            reponse["statut"] = "succes"
            reponse["message"] = "Compte marchand modifié"
        except:
            reponse["statut"] = "echec"
            reponse["message"] = "Echec de la modification du compte"
        reponse = json.dumps(reponse)
        mimetype = "application/json"
        return HttpResponse(reponse, mimetype)
    else:
        return HttpResponse("Requete incorrect")

@login_required(login_url='/connexion')
def liste_compte(request):
    module(request, "recette")
    context = {}
    context["nb_compte_airtel"] = CompteMarchand.objects.filter(type_compte__libelle="Airtel Money").count()
    context["nb_compte_moov"] = CompteMarchand.objects.filter(type_compte__libelle="Mobi Cash").count()
    context["nb_compte"] = CompteMarchand.objects.all().count()
    context["comptes"] = CompteMarchand.objects.all()
    context["magasins"] = Magasin.objects.all()
    context["t_mags"] = TypeCompte.objects.all()
    return render(request,"recette/liste_comptes.html",context)
@login_required(login_url='/connexion')
def page_magasin(request):
    module(request, "recette")
    return render(request,"recette/page_magasin.html")

@login_required(login_url='/connexion')
def type_mag_dans_ville(request,nom_ville,lib_type_mag):
    module(request, "recette")
    ville = get_object_or_404(Ville,nom_ville=nom_ville)
    type_mag = get_object_or_404(TypeMagasin,libelle=lib_type_mag)
    return render(request,"recette/type_mag_dans_ville.html",{"type_mag":type_mag,"ville":ville})
@login_required(login_url='/connexion')
def recette_airtel(request):
    module(request, "recette")
    return render(request,"recette/recette_airtel.html")
@login_required(login_url='/connexion')
def recette_moov(request):
    module(request, "recette")
    return render(request,"recette/recette_airtel.html")
@login_required(login_url='/connexion')
def voir_details_compte(request,id):
    module(request, "recette")
    compte = get_object_or_404(CompteMarchand,pk=id)
    return render(request,"recette/detail_compte.html",{"compte":compte})
def index2(request):
    return render(request,"reconciliation/formlayouts.html")

def index4(request):
    return render(request,"reconciliation/userlist.html")

def index5(request):
    return render(request,"reconciliation/sweetalert.html")

def page_des_recettes(request):
    return render(request,"reconciliation/recette.html")

def connexion(request):
    form = LoginForm()
    user = User.objects.get(email="gabon.smart2022@gmail.com")
    print(user.is_active)
    user.is_active=True
    user.save()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if User.objects.filter(email=email).exists():
                user = get_object_or_404(User,email=email)
                username = user.username
                user = authenticate(username=username,password=password)
                if user is not None:
                    if user.is_active:
                        try:
                            login(request,user)
                            utilisateur = Utilisateur.objects.get(user=user)
                            utilisateur.est_connecte = True
                            utilisateur.save()
                            request.session["username"] = user.username
                            request.session["userid"] = user.id
                            request.session["nom"] = user.last_name
                            request.session["prenom"] = user.first_name
                            request.session["email"] = user.email
                            return redirect("reco_gest:choisir_module")
                        except Exception as e:
                            print(e)
                            messages.add_message(request, messages.WARNING, "Email ou mot de passe incorrect")
                            return render(request,"reconciliation/login.html",{"form":form})
                    else:
                        messages.add_message(request, messages.WARNING, "Cet utilisateur n'est pas activé. Veuillez vous adresser à l'administrateur")
                        return render(request, "reconciliation/login.html", {"form": form})
                else:
                    messages.add_message(request, messages.WARNING, "Email ou mot de passe incorrect")
                    print("mmmmm")
                    return render(request, "reconciliation/login.html", {"form": form})
            else:
                messages.add_message(request, messages.WARNING, "Email ou mot de passe incorrect")
                return render(request, "reconciliation/login.html", {"form": form})
        else:
            return render(request, "reconciliation/login.html", {"form": form})
    return render(request,"reconciliation/login.html",{"form":form})

@login_required(login_url='/connexion')
def deconnexion(request):
    logout(request)
    return redirect(reverse("reco_gest:connexion"))

@login_required(login_url='/connexion')
def profile(request,id):
    module(request, "users")
    user = get_object_or_404(User,pk=id)
    agent = get_object_or_404(Utilisateur,user=user)
    return render(request,"reconciliation/profile.html",{"agent":agent})

@login_required(login_url='/connexion')
def associer_boutique_compte(request,id):
    if is_ajax(request=request) and request.method == "POST":
        pass

def dashboard_reporting(request):
    module(request, "reporting")
    return render(request,"reporting/dashboard_reporting.html")

def reporting_provinces(request):
    module(request, "reporting")
    provinces = Province.objects.all()
    return render(request,"reporting/reporting_provinces.html",{"provinces":provinces})

def reporting_villes(request):
    module(request, "reporting")
    villes = Ville.objects.all()
    return render(request,"reporting/reporting_ville.html",{"villes":villes})

def reporting_magasins(request):
    module(request, "reporting")
    t_magasins = TypeMagasin.objects.all()
    return render(request,"reporting/reporting_type_magasin.html",{"t_magasins":t_magasins})

def detail_magasin(request,id):
    module(request, "recette")
    magasin = get_object_or_404(Magasin,pk=id)
    compte_a = CompteMarchand.objects.filter(magasin=magasin,type_compte__libelle="Airtel Money")
    compte_m = CompteMarchand.objects.filter(magasin=magasin,type_compte__libelle="Mobi Cash")
    return render(request,"recette/detail_magasin.html",{"magasin":magasin,"compte_a":compte_a,"compte_m":compte_m})

def recette_par_magasin(request):
    module(request, "recette")
    id = 2
    typemags = TypeMagasin.objects.all()
    return render(request,"recette/recette_par_magasin.html",{"typemags":typemags,"id":id})

def changer_module(request):
    if is_ajax(request=request) and request.method=="POST":
        module = request.POST.get("module")
        request.session["module"] = module
        reponse = {"module":module}
        mimetype = "application/json"
        reponse = json.dumps(reponse)
        return HttpResponse(reponse, mimetype)
    else:
        return HttpResponse("Requete non authorisée")
# Create your views here.
