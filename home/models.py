from django.db import models

# Create your models here.

# class Settings(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     logo = models.ImageField('Logo', upload_to="SettingsImg/Logo", null=True, blank=True)
#     phoneNumber = models.CharField("Numéro de téléphone", max_length=14, null=True, blank=True)
#     email = models.CharField("Adresse email", max_length=255, null=True, blank=True)
#     location = models.CharField("Localisation", max_length=255, null=True, blank=True)
#     actif = models.BooleanField(default=False, unique=True)

#     def __str__(self):
#         return self.name

#     # def imageUrl(self):
#     #     try:
#     #         url = self.image.url
#     #     except:
#     #         url = ''
#     #     return url

#     class Meta:
#         verbose_name_plural = "Paramètres du site"

# class Slide(models.Model):    
#     name = models.CharField(max_length=100, null=True, blank=True)
#     slide1 = models.ImageField('Slide1', upload_to="SettingsImg/Slide", null=True, blank=True)
#     slide2 = models.ImageField('Slide2', upload_to="SettingsImg/Slide", null=True, blank=True)
#     slide3 = models.ImageField('Slide3', upload_to="SettingsImg/Slide", null=True, blank=True)
#     actif = models.BooleanField(default=False, unique=True)

#     def __str__(self):
#         return self.name


# class Promotion(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     promotion = models.CharField("Promotion1", max_length=255, null=True, blank=True)
#     promotion1 = models.CharField("Promotion2", max_length=255, null=True, blank=True)
#     promotion2 = models.CharField("Promotion3", max_length=255, null=True, blank=True)
#     actif = models.BooleanField(default=False, unique=True)

#     def __str__(self):
#         return self.name
