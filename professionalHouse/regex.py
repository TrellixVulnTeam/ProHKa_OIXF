from os import error
import re

from django.db.models import fields

regex = '^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
phoneReg = '^(2|6)[0-9]{8}$'
charReg = '^[a-zA-Z]+[\D]+?$'
passwordReg = '^(?=(.*[0-9]))(?=.*[a-z])(?=(.*[A-Z]))(?=(.*)).{5,}$'
priceReg = '^[+]?([1-9]\d*(\.\d*[1-9])?|0\.\d*[1-9]+)|\d+(\.\d*[1-9])?$'


def checkMail(email):
    if re.search(regex, email):
        return True
    return False


def setEmailError(key, field, error):
    if field:
        if checkMail(field) == False:
            error.append({key: 'Adresse Email invalide'})
        else:
            return field
    else:
        error.append({key: 'Ce champ est requis'})


def setEmailErrorNotRequire(key, field, error):
    if field:
        if checkMail(field) == False:
            error.append({key: 'Adresse Email invalide'})
        else:
            return field
    # else:
    #     error.append({key: 'Ce champ est requis'})


def checkCharField(field, minLength):
    return (len(field) > minLength and len(field) < 255) and (re.match(charReg, field))


def setErrorKeyField(key, request, minLength, error):
    if key not in request.POST:
        error.append({key: 'Ce champ est requis'})
    else:
        if checkCharField(request.POST[key], minLength) == False:
            error.append(
                {key: f'Ce champ doit contenir au moins {minLength} caractères'})
        elif len(request.POST[key]) == 0 or request.POST[key] == 'null' or request.POST[key] == None:
            error.append({key: 'Ce champ est obligatoire'})
        else:
            return request.POST[key]


def chekKeyExists(key, request):
    # verifie si une cle existe dans une requete
    if key in request.POST:
        return request.POST[key]
    elif key in request.FILES:
        return request.FILES[key]
    else:
        pass


def setErrorField(field, fieldName, minLength, error):
    if field:
        if checkCharField(field, minLength) == False:
            error.append(
                {fieldName: f'Ce champ doit contenir au moins {minLength} caractères'})
    else:
        error.append({fieldName: 'Ce champ est requis'})


def checkPhoneNumber(field):
    if re.match(phoneReg, field):
        return True
    return False


def setPhoneError(key, field, error):
    if field:
        if checkPhoneNumber(field) == False:
            error.append({key: 'Numero de téléphone invalide'})
        else:
            return field
    else:
        error.append({key: 'Ce champ est requis'})


def checkKeyInData(key, data, error):
    if key in data:
        return data[key]
    else:
        error.append({key: f"Vous devez choisir un(e) {key}"})


def checkLenOfField(key, sentence, lenght, error):
    if len(sentence) == 0 or sentence == None:
        error.append({key: "Ce champ est réquis"})
    elif len(sentence) < lenght:
        error.append(
            {key: f"ce champ doit contenir au moins {lenght} caractères"})
    else:
        return sentence


def checkLenAndCompareNumber(key, sentence, error):
    if len(sentence) == 0 or sentence == None:
        error.append({key: "Ce champ est réquis"})
    elif int(sentence) > 5:
        error.append(
            {key: "Les notes sont comprises entre 0 et 5"})
    else:
        return sentence


def checkPrice(field):
    if re.match(priceReg, field):
        return True
    return False


def setPriceError(field, fieldName, error):
    if field:
        if checkPrice(field) == False:
            error.append(
                {fieldName: 'Ce champ ne doit contenir que des chiffes positifs'})
        # else:
        #     error.append({fieldName: 'Ce champ est requis'})


def checkPassword(password1):
    if re.search(passwordReg, password1):
        return True
    return False


def setPassword(field, error):
    if field:
        if checkPassword(field) == False:
            error.append(
                {'password1': 'Votre mot de passe doit contenir au moins 5 caractères contenant une majuscule et un chiffre au moins'})
    else:
        error.append({'password1': 'Ce champ est requis'})


def checkPathDelete(oldPathTab, newPathTab, newTab, delTab):
    # verifie les chemins a supprimer
    for el in oldPathTab:
        if el in newPathTab:
            newTab.append(el)
        else:
            delTab.append(el)


def checkExtensionImg(img, key, error):
    extensions = ['jpg', 'jpeg']
    if img == None:
        error.append(
            {key: 'Veuillez sélectionner une image principale'}
        )
    else:
        name = str(img).split(".")[-1]
        if not name in extensions:
            error.append(
                {key: 'Veuillez choisir une image au format jpg ou jpeg'}
            )
        else:
            return img


def checkIfNumber(field, key, error):
    if field == '' or field == None:
        error.append(
            {key: "Ce champ est requis"}
        )
    elif not field.isnumeric():
        error.append(
            {key: "Vous devez entrer des chiffress"}
        )
    else:
        return field
