from django import forms
from django.core.exceptions import ValidationError
from gestion_reconciliations.models import Province, Ville, TypeMagasin, Magasin, CompteMarchand

err_msg = {"required":"Veuillez renseigner ce champs !","invalid":"Valeur de champs invalides"}

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=30,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"username"}))
    email = forms.EmailField(max_length=50,required=True, error_messages=err_msg,widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))
    password = forms.CharField(required=True,max_length=50, error_messages=err_msg, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}))
    password_confirm = forms.CharField(required=True,max_length=50, error_messages=err_msg, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}))

class ProvinceForm(forms.Form):
    codeprovince = forms.CharField(required=True, max_length=30, error_messages=err_msg,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Code de la province"}))
    nomprovince = forms.CharField(required=True, max_length=30, error_messages=err_msg,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom de la province"}))

    def clean_codeprovince(self):
        data = self.cleaned_data["codeprovince"]
        if Province.objects.filter(code=data).exists():
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

class TypeMagasinForm(forms.Form):
    libelle = forms.CharField(required=True, max_length=50,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Libellé du type"}))
    code = forms.CharField(required=False, max_length=50,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Code de du type"}))

    def clean_libelle(self):
        data = self.cleaned_data["libelle"]
        if TypeMagasin.objects.filter(libelle=data).exists():
            raise ValidationError("Un type de magasin avec ce libellé existe déjà !")
        return data
class TypeCompteForm(forms.Form):
    libelle = forms.CharField(required=True, max_length=50,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Libellé du type"}))
    code = forms.CharField(required=False, max_length=50,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Code de du type"}))

    def clean_libelle(self):
        data = self.cleaned_data["libelle"]
        if TypeMagasin.objects.filter(libelle=data).exists():
            raise ValidationError("Un type de magasin avec ce libellé existe déjà !")
        return data

class VilleForm(forms.Form):
    nomville = forms.CharField(required=True, max_length=50, error_messages=err_msg,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom de la ville"}))
    provinces = forms.ModelChoiceField(queryset=Province.objects.all(),widget=forms.Select(attrs={"class":"form-control","placeholder":"Province"}))

    def clean_nomville(self):
        data = self.cleaned_data["nomville"]
        if Ville.objects.filter(nom_ville=data).exists():
            raise ValidationError("Une ville avec ce nom existe déjà !")
        return data


class CompteForm(forms.Form):
    libelle = forms.CharField(required=True, max_length=100, error_messages=err_msg, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Libellé du compte"}))
    numero = forms.CharField(required=True, max_length=100, error_messages=err_msg, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro de téléphone"}))

    def clean_numero(self):
        data = self.cleaned_data["numero"]
        if CompteMarchand.objects.filter(numero_telephone=data).exists():
            raise ValidationError("Un compte avec ce numéro existe déja")
        return data

class MagasinForm(forms.Form):
    type_magasin = forms.ModelChoiceField(required=True,queryset=TypeMagasin.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))
    ville = forms.ModelChoiceField(required=True,queryset=Ville.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))
    nom_magasin = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Nom du magasin"}))
    adresse = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Adresse du magasin"}))
    commune = forms.CharField(required=True, max_length=100,error_messages=err_msg,widget=forms.TextInput(attrs={"class":"form-control","placeholder": "Commune du magasin"}))
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


