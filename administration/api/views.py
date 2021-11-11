import base64
import json
import datetime
from django.core.files.base import ContentFile
from administration.api.serializers import *
from administration.models import *
from administration.utils import *
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from professionalHouse.regex import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser


class ProfileRegistrationAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        userEmployers = UserRegistration.objects.filter(
            user_id=None).order_by('-updated')
        serializers = UserRegistrationSerializers(userEmployers, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        error = []
        errors = {}
        fileTab = []

        if request.method == "POST":
            data = JSONParser().parse(request)
            names = checkLenOfField('name', data['name'], 1, error)
            surname = checkLenOfField('surname', data['surname'], 1, error)
            email = setEmailErrorNotRequire('email', data['email'], error)
            phone = checkLenOfField('phone', data['phone'], 1, error)
            dateBorn = checkLenOfField('dateBorn', data['dateBorn'], 1, error)
            placeBorn = checkLenOfField(
                'placeBorn', data['placeBorn'], 1, error)
            religion = checkLenOfField('religion', data['religion'], 1, error)
            situation = checkLenOfField(
                'situation', data['situation'], 1, error)
            age = checkLenOfField('age', str(data['age']), 1, error)
            nbrChildren = checkLenOfField(
                'children', str(data['children']), 1, error)
            cityLive = checkLenOfField('city', data['city'], 1, error)
            language = checkLenOfField('language', data['language'], 1, error)
            # mainImg = checkExtensionImg(request.FILES.get('file'), 'mainImg', error)
            mainImg = data['mainImg']
            othersImg = list(data['fileUpload'])
            availability = data['availability']
            # availability = CheckTrueFalseLowerCase(availability)
            extensions = ['jpg', 'jpeg']
            for files in othersImg:
                if files['fileToSend']:
                    name = str(files['fileToSend']['name']).split(".")[-1]
                    if not name in extensions:
                        errors['file'] = 'Votre fichier doit etre au format jpg, jpeg'
                else:
                    errors['file'] = "Veuillez sélectionner au moins un fichier et ajouter un titre"

            if language == 'Choisir...':
                errors['language'] = "Ce champ est réquis"

            for data in error:
                for dat in data:
                    errors[dat] = data[dat]

            if len(error) == 0 and len(errors) == 0:

                slug = name + id_generator()
                url = '/media/'
                user = UserRegistration.objects.create(slug=slug, name=names, surname=surname, email=email, phoneNumber=phone,
                                                       dateBorn=dateBorn, placeBorn=placeBorn, residence=cityLive, languages=language, mainImg='mainImg',
                                                       status=availability, age=int(age), religion=religion, situation=situation, children=int(nbrChildren))
                user.save()
                for file in othersImg:
                    name = file['fileToSend']['name']
                    fileSave = file['fileToSend']['file']
                    # format est le format du fichier et imgstr est le fichier en string
                    format, imgstr = fileSave.split(';base64,')
                    ext = format.split('/')[-1]
                    unique = id_generator()
                    user.otherImg = ContentFile(
                        base64.b64decode(imgstr), name=unique+name)
                    user.save()
                    fileTab.append({"ext": ext,
                                    "file": url+unique+file['fileToSend']['name'].replace(' ', '_').replace("'", "").replace("(", "").replace(")", "")})
                user.saveOtherImg = json.dumps(fileTab)
                user.save()
                serializer = UserRegistrationSerializers(user)
                # SaveForImg.saveImg(files, user, UserRegistration, slug, url, tabl)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileEditAPIView(APIView):
    def get_object(self, pk):
        profile = get_object_or_404(UserRegistration, pk=int(pk))
        return profile

    def get(self, request, pk):
        # profile = self.get_object(pk)
        # serializer = UserRegistrationSerializers(profile)
        return Response('serializer.data', status=status.HTTP_200_OK)

    def put(self, request, pk):
        profile = self.get_object(pk)
        if request.method == 'PUT':
            data = JSONParser().parse(request)
            owner = data['data']
            profile.owner_id = int(owner)
            profile.save()
            serializer = UserRegistrationSerializers(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        profile = files = mainImg = ''
        profile = self.get_object(pk)
        mainImg = "/" + str(profile.mainImg)
        os.remove(settings.MEDIA_ROOT + mainImg)
        files = json.loads(profile.saveOtherImg)
        deletePathImage(files)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GlobalSettingAPIView(APIView):

    def get(self, request, format=None):
        slides = Slides.objects.all().order_by('updated')[:3]
        serializers = SettingsSerializers(slides, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        error = []
        if request.method == 'POST':
            data = request.POST
            title = checkLenOfField('title', data['title'], 1, error)
            slideImg = request.FILES.get('slide')
            availability = data['availability']
            # availability = CheckTrueFalseLowerCase(availability)

            if len(error) == 0:
                slide = Slides.objects.create(
                    title=title, slide=slideImg, status=availability)

            return Response('errors', status=status.HTTP_201_CREATED)


class ReceiveCommandAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        commands = ReceiveCommand.objects.all().order_by('updated')
        serializers = ReceiveCommandSerializers(commands, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        error = []
        errors = {}
        if request.method == 'POST':
            data = request.POST
            civility = data['civility']
            profile = data['profile']
            name = checkLenOfField('name', data['name'], 1, error)
            surname = checkLenOfField('surname', data['surname'], 1, error)
            email = checkLenOfField('email', data['email'], 1, error)
            phone = checkLenOfField('phone', data['phone'], 1, error)
            if civility == "Choisir...":
                errors["civility"] = "Veillez choisir une civilité"
            if error:
                for data in error:
                    for dat in data:
                        errors[dat] = data[dat]
            if len(error) == 0 and len(errors) == 0:
                command = ReceiveCommand.objects.create(user_id=int(profile), civility=civility, name=name, surname=surname,
                                                        email=email, phone=phone)
                command.save()
                return JsonResponse({'data': 'success'}, status=201, content_type="application/json")
            else:
                return JsonResponse(errors, status=400)


class CommandEditAPIView(APIView):
    def get_object(self, pk):
        command = get_object_or_404(ReceiveCommand, pk=int(pk))
        return command

    def get(self, request, pk):
        command = self.get_object(pk)
        serializer = ReceiveCommandSerializers(command)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        command = self.get_object(pk)
        if request.method == 'PUT':
            data = JSONParser().parse(request)
            statu = data['status']
            command.status = statu
            command.save()
            serializer = ReceiveCommandSerializers(command)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        command = self.get_object(pk)
        command.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactUsAPIView(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all().order_by('-updated')
        serializers = MessageSerializers(messages, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        error = []
        errors = {}
        if request.method == 'POST':
            data = request.POST
            name = checkLenOfField('name', data['name'], 1, error)
            email = setEmailError('email', data['email'], error)
            phone = setPhoneError('phone', data['phone'], error)
            subject = checkLenOfField('subject', data['subject'], 5, error)
            message = checkLenOfField('message', data['message'], 10, error)
            if error:
                for data in error:
                    for dat in data:
                        errors[dat] = data[dat]
            if len(error) == 0 and len(errors) == 0:
                message = Message.objects.create(
                    name=name, email=email, phone=phone, object=subject, message=message)
                message.save()
                return JsonResponse({'data': 'success'}, status=201, content_type="application/json")
            else:
                return JsonResponse(errors, status=400)


class MessageEditAPIView(APIView):
    def get_object(self, id):
        message = get_object_or_404(Message, pk=int(id))
        return message

    def get(self, request, pk):
        message = self.get_object(pk)
        serializer = MessageSerializers(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        message = self.get_object(id)
        if request.method == 'PUT':
            data = JSONParser().parse(request)
            statu = data['data']
            message.status = statu
            message.save()
        return Response("message update", status=status.HTTP_200_OK)

    def delete(self, request, id):
        message = self.get_object(id)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendProposition(APIView):
    def post(self, request):
        urls = []
        profile = []
        if request.method == 'POST':
            data = JSONParser().parse(request)
            idClient = data['id']
            profil = data['profile']
            for idProfile in profil:
                profile.append(str(idProfile['id']))
            emailClient = User.objects.get(id=int(idClient)).email
            for idProfile in profile:
                profileUser = UserRegistration.objects.get(id=int(idProfile))
                url = "http://127.0.0.1:8000/home/gallery/{}/".format(
                    int(idProfile))
                urls.append(url)
                if profileUser.user_id:
                    profileUser.user_id = int(idClient)
                    profileUser.save()
            sendMessage("Propositions des profils suite à votre besoin",
                        'email/urls.html', {'urls': urls}, settings.EMAIL_HOST_USER, [emailClient])
            removeOwner = UserRegistration.objects.get(
                id=int(idClient)).updated
            timeUpdate = removeOwner.strftime("%Y-%m-%d")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return Response("email send", status=status.HTTP_200_OK)


class ChoiceCLient(APIView):
    def post(self, request):
        if request.method == 'POST':
            emailClient = request.user.email
            idProfile = request.POST['idProfile']
            profile = UserRegistration.objects.get(id=int(idProfile))
            sendMessage("Profil choisi par le client", 'email/choiceClient.html',
                        {'profile': profile}, emailClient, [settings.EMAIL_HOST_USER])
        return Response("success", status=status.HTTP_200_OK)
