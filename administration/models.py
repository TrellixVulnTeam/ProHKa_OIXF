from string import punctuation
from django.db import models
from django.utils.translation import activate
from authentication.models import *

# Create your models here.


class UserRegistration(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    slug = models.CharField(max_length=50, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(
        "Adresse email", max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(
        "Numéro de téléphone", max_length=14, null=True, blank=True)
    dateBorn = models.CharField(
        "Date de naissance", max_length=20, null=True, blank=True)
    placeBorn = models.CharField(
        "Lieu de naissance", max_length=50, null=True, blank=True)
    residence = models.CharField(
        "Lieu de résidence", max_length=50, null=True, blank=True)
    languages = models.CharField(
        "Langue parlée", max_length=255, null=True, blank=True)
    age = models.IntegerField('Age', null=True, blank=True)
    children = models.IntegerField("Nombre d'enfants", null=True, blank=True)
    religion = models.CharField(
        "Religion", max_length=255, null=True, blank=True)
    situation = models.CharField(
        "Situation matrimoniale", max_length=255, null=True, blank=True)
    mainImg = models.ImageField(
        'Image principale', upload_to="Person/mainImg", null=True, blank=True)
    otherImg = models.ImageField(
        'Autres images', upload_to="Person/otherImg", null=True, blank=True)
    saveOtherImg = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


class Slides(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    slide = models.ImageField(
        'Image slide', upload_to="settings/slides", null=True, blank=True)
    indexImg = models.ImageField(
        'Image Bas de slide', upload_to="settings/shortView", null=True, blank=True)
    status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Slides"


class ReceiveCommand(models.Model):
    user = models.ForeignKey(
        UserRegistration, on_delete=models.CASCADE, null=True, blank=True)
    civility = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(max_length=15, default="ouvert")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


class GlobalSetting(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(
        'Image slide', upload_to="settings/logos", null=True, blank=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    whatsapp = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    localisation = models.CharField(max_length=255, null=True, blank=True)
    aboutUs = models.TextField(null=True, blank=True)
    pictureAboutUs = models.ImageField(
        'Image A propos de nous', upload_to="settings/about", null=True, blank=True)
    longAboutUs = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.BooleanField(unique=True, default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    object = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, default='non lu')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email


class EvaluationFile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    profileUser = models.ForeignKey(
        UserRegistration, on_delete=models.CASCADE, null=True, blank=True)
    punctuation = models.IntegerField(null=True, blank=True)
    adaptation = models.IntegerField(null=True, blank=True)
    respect = models.IntegerField(null=True, blank=True)
    iniative = models.IntegerField(null=True, blank=True)
    finalNote = models.IntegerField(null=True, blank=True)
    decision = models.BooleanField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.profileUser
