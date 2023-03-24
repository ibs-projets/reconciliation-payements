from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile


class Roles(models.Model):
    admin_general = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    caissier = models.BooleanField(default=False)
    visiteur = models.BooleanField(default=True)
    directeur = models.BooleanField(default=False)

class Utilisateur(models.Model):
    ville = models.ForeignKey("Ville",on_delete=models.DO_NOTHING,null=True,blank=True)
    adresse = models.CharField(max_length=200,default="")
    photo = models.ImageField(upload_to="utilisateurs/photos",null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=3)
    telephone = models.CharField(max_length=10)
    magasin = models.ForeignKey("Magasin",on_delete=models.SET_NULL,null=True,blank=True)
    est_connecte = models.BooleanField(default=False)
    roles = models.OneToOneField(Roles,on_delete=models.SET_NULL,null=True,blank=True)


class InfosConnexion(models.Model):
    utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    date_connextion = models.DateTimeField(auto_now_add=True)
    date_deconnexion = models.DateTimeField()

class Affectation(models.Model):
    Utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    magasin = models.ForeignKey("Magasin",on_delete=models.CASCADE)
    dte_affectation = models.DateTimeField(auto_now_add=True)


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)

class Province(models.Model):
    code = models.CharField(max_length=10)
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Ville(models.Model):
    province = models.ForeignKey(Province,on_delete=models.CASCADE,related_name="villes")
    nom_ville = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_ville

class TypeMagasin(models.Model):
    image = models.ImageField(null=True,blank=True,upload_to="typemagasin/images")
    code_type = models.CharField(max_length=30,blank=True,null=True)
    libelle = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.libelle

class Magasin(models.Model):
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name="mags")
    type_magasin = models.OneToOneField(TypeMagasin,on_delete=models.SET_NULL,null=True,blank=True,related_name="magasins")
    nom_magasin = models.CharField(max_length=50,null=True,blank=True)
    adresse = models.CharField(max_length=100)
    commune = models.CharField(max_length=100,null=True,blank=True)
    point_repere = models.CharField(max_length=50,null=True,blank=True)
    chef = models.OneToOneField(Utilisateur,on_delete=models.SET_NULL,related_name="responsable",null=True,blank=True)
    telephone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def liste_comptes(self):
        liste_comptes = []
        for compte in CompteMarchand.objects.filter(magasin=self):
            liste_comptes.append(compte.libelle_compte)
        return liste_comptes

    def possede_compte(self):
        if CompteMarchand.objects.filter(magasin=self):
            return True

    def __str__(self):
        return "{0} - {1}".format(self.type_magasin.libelle,self.nom_magasin)

class TypeCompte(models.Model):
    code = models.CharField(max_length=30,null=True,blank=True)
    libelle = models.CharField(max_length=30)

    def __str__(self):
        return self.libelle

class CompteMarchand(models.Model):
    magasin = models.ForeignKey(Magasin,on_delete=models.SET_NULL,null=True,blank=True,related_name="comptes")
    type_compte = models.ForeignKey(TypeCompte,on_delete=models.SET_NULL,blank=True,null=True)
    libelle_compte = models.CharField(max_length=50)
    numero_telephone = models.CharField(max_length=10)
    date_creation = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    compte = models.ForeignKey(CompteMarchand,on_delete=models.SET_NULL,null=True,blank=True)
    ref_transaction = models.CharField(max_length=50)
    nb_operation = models.IntegerField()
    charges = models.DecimalField(max_digits=8, decimal_places=2)
    msisdn = models.CharField(max_length=50)
    status = models.CharField(max_length=10,blank=True,null=True)
    devise = models.CharField(max_length=10,blank=True,null=True)
    client = models.CharField(max_length=100)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ref_transaction






# Create your models here.
