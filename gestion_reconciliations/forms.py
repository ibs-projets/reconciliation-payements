from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from gestion_reconciliations.models import Province, Ville, TypeMagasin, Magasin, CompteMarchand, TypeCompte

err_msg = {"required":"Veuillez renseigner ce champs !","invalid":"Valeur de champs invalides"}

class UserForm(forms.Form):
    nom = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nom de l'utlisateur"}))
    prenom = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Prénom de l'utlisateur"}))
    adresse = forms.CharField(required=True, max_length=200,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Adresse"}))
    telephone = forms.CharField(required=True, max_length=10,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Téléphone"}))
    email = forms.CharField(required=True, max_length=30, error_messages=err_msg, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))
    admin = forms.BooleanField(label="Administrateur",required=False,disabled=False,widget=forms.CheckboxInput())
    operateur = forms.BooleanField(label="Consultant",required=False,disabled=True,widget=forms.CheckboxInput(attrs={'checked': True}))
    #caissier = forms.BooleanField(label="Caissier",required=False,disabled=False,widget=forms.CheckboxInput())

    def clean_nom(self):
        data = self.cleaned_data["nom"]
        if User.objects.filter(username=data):
            raise ValidationError("Un utilisateur avec ce nom existe déjà")
        return data
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50,required=True, error_messages=err_msg,widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Identifiant"}))
    password = forms.CharField(required=True,max_length=50, error_messages=err_msg, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}))

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = "__all__"
    code = forms.CharField(required=True, max_length=30, error_messages=err_msg,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Code de la province"}))
    nom = forms.CharField(required=True, max_length=30, error_messages=err_msg,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom de la province"}))

    def clean_code(self):
        data = self.cleaned_data["code"]
        if Province.objects.filter(code=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Une province avec ce code existe déja !")
        return data

    def clean_nomprovince(self):
        data = self.cleaned_data["nomprovince"]
        if Province.objects.filter(nom=data).exists():
            raise ValidationError("Une province avec ce nom existe déja !")
        return data


class VilleForm(forms.Form):
    nom_ville = forms.CharField(label="Nom de la ville",required=True, max_length=50,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control"}))
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': "form-control"  # is this POSSIBLE?
        })
    )

class TypeMagasinForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(TypeMagasinForm,self).__init__(*args,**kwargs)
        self.fields["idtypemagasin"].initial = ""

    class Meta:
        model = TypeMagasin
        fields = ["code_type","libelle"]
    libelle = forms.CharField(required=True, max_length=50,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Nom du type de magasin"}))
    code_type = forms.CharField(required=False, max_length=50,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Code du type de magasin"}))
    idtypemagasin = forms.CharField(required=False,max_length=5,widget=forms.TextInput(attrs={"id":"idtypemagasin"}))



    def clean_libelle(self):
        libelle = self.cleaned_data["libelle"]
        if TypeMagasin.objects.filter(libelle__exact=libelle).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Un type de magasin avec ce libellé!")
        return self.cleaned_data["libelle"]
class TypeCompteForm(forms.Form):
    LIBELLES = (("Airtel Money","Airtel Money"),("Moov Money","Moov Money"))
    libelle = forms.ChoiceField(required=True,choices=LIBELLES,error_messages=err_msg,widget=forms.Select(attrs={"class":"form-control","placeholder": "Libellé du type"}))
    code = forms.CharField(required=True, max_length=50,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Code opérateur"}))

    def clean_libelle(self):
        data = self.cleaned_data["libelle"]
        if TypeMagasin.objects.filter(libelle=data).exists():
            raise ValidationError("Un type de magasin avec ce libellé existe déjà !")
        return data

class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields = "__all__"
    nom_ville = forms.CharField(required=True, max_length=50, error_messages=err_msg,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom de la ville"}))
    province = forms.ModelChoiceField(empty_label=None,queryset=Province.objects.all(),widget=forms.Select(attrs={"class":"form-control","placeholder":"Province"}))

    def clean_nomville(self):
        data = self.cleaned_data["nom_ville"]
        if Ville.objects.filter(nom_ville=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Une ville avec ce nom existe déjà !")
        return data


class CompteForm(forms.Form):
    libelle = forms.CharField(required=True, max_length=100, error_messages=err_msg, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro marchand"}))
    numero = forms.CharField(required=True, max_length=100, error_messages=err_msg, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro de téléphone"}))
    magasins = forms.ModelChoiceField(empty_label=None,queryset=Magasin.objects.all(),widget=forms.Select(attrs={"class":"form-control","placeholder":"Magasins"}))
    typecompte = forms.ModelChoiceField(empty_label=None,queryset=TypeCompte.objects.all(),widget=forms.Select(attrs={"class":"form-control","placeholder":"Type de compte"}))

    def clean_numero(self):
        data = self.cleaned_data["numero"]
        if CompteMarchand.objects.filter(numero_telephone=data).exists():
            raise ValidationError("Un compte avec ce numéro existe déja")
        return data

class AssocierCompteMagasinForm(forms.Form):
    libelle = libelle = forms.CharField(required=True, max_length=100, error_messages=err_msg, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro marchand"}))
    numero = forms.CharField(required=True, max_length=100, error_messages=err_msg, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro de téléphone"}))
    typecompte = forms.ModelChoiceField(empty_label=None,queryset=TypeCompte.objects.all(), widget=forms.Select(attrs={"class": "form-control", "placeholder": "Type de compte"}))
    def clean_numero(self):
        data = self.cleaned_data["numero"]
        if CompteMarchand.objects.filter(numero_telephone=data).exists():
            raise ValidationError("Un compte avec ce numéro existe déja")
        return data


class MagasinForm(forms.ModelForm):
    class Meta:
        model = Magasin
        fields = "__all__"
    type_magasin = forms.ModelChoiceField(empty_label=None,required=True,queryset=TypeMagasin.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))
    ville = forms.ModelChoiceField(empty_label=None,required=True,queryset=Ville.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))
    nom_magasin = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Nom du magasin"}))
    adresse = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Quartier"}))
    commune = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Arrondissement du magasin"}))
    point_repere = forms.CharField(max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Point de repère"}))
    telephone = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Téléphone du magasin"}))
    email = forms.CharField(max_length=50,error_messages=err_msg,widget=forms.EmailInput(attrs={"class":"form-control","placeholder": "Email"}))
    latitude = forms.FloatField(required=True, min_value=0,widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Latitude", "step": "0.000000001"}))
    longitude = forms.FloatField(required=True, min_value=0,widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Longitude", "step": "0.000000001"}))

    def clean_nom_magasin(self):
        nom_magasin = self.cleaned_data["nom_magasin"]
        ville = self.cleaned_data["ville"]
        if Magasin.objects.filter(ville=ville,nom_magasin=nom_magasin).exists():
            raise ValidationError("Un magasin avec ce nom existe déjà dans la meme ville !")
        return nom_magasin

class EditMagasinForm(forms.ModelForm):
    class Meta:
        model = Magasin
        fields = "__all__"


