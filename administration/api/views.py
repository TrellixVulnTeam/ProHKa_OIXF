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
from professionalHouse.pagination import *
from rest_framework.generics import ListAPIView
# from rest_framework import filters


class ProfileListing(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserRegistrationSerializers

    def get_queryset(self):
        queryList = UserRegistration.objects.all().order_by("-updated")
        search = self.request.query_params.get('search')
        if search == "all":
            queryList = UserRegistration.objects.all().order_by("-updated")
        else:
            queryList = queryList.filter(
                name__icontains=search).order_by("-updated")
        return queryList


class ProfileRegistrationAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # queryset = User.objects.all()
    # serializer_class = UserRegistrationSerializers
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ['name', 'surname']
    # pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
        s = request.GET.get('s')
        userEmployers = UserRegistration.objects.filter(
            user_id=None).order_by('-updated')
        if s:
            userEmployers = UserRegistration.objects.filter(name__icontains=s)
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


class ContactUsAPIView(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all().order_by('-updated')
        serializers = MessageSerializers(messages, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        error = []
        errors = {}
        if request.method == 'POST' and request.user.is_authenticated:
            data = request.POST
            name = request.user.name + " " + request.user.username
            email = request.user.email
            phone = request.user.phone
            subject = checkLenOfField('subject', data['subject'], 5, error)
            message = checkLenOfField('message', data['message'], 10, error)
            if error:
                for data in error:
                    for dat in data:
                        errors[dat] = data[dat]
            if len(error) == 0 and len(errors) == 0:
                message = Message.objects.create(
                    name=name, email=email, phone=phone, object=subject, message=message, authenticated=True)
                message.save()
                return JsonResponse({'data': 'success'}, status=201, content_type="application/json")
            else:
                return JsonResponse(errors, status=400)

        elif request.method == 'POST' and not request.user.is_authenticated:
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
                    name=name, email=email, phone=phone, object=subject, message=message, authenticated=False)
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
            try:
                emailClient = User.objects.get(id=int(idClient)).email
            except User.DoesNotExist:
                emailClient = None
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


class EvaluateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        evaluation = EvaluationFile.objects.all().order_by('updated')
        serializers = EvaluationFileSerializers(evaluation, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, format=None):
        error = []
        errors = {}
        if request.method == 'POST':
            data = request.POST
            punctuality = checkLenAndCompareNumber(
                'punctuality', data['punctuality'], error)
            adaptation = checkLenAndCompareNumber(
                'adaptation', data['adaptation'], error)
            respect = checkLenAndCompareNumber(
                'respect', data['respect'], error)
            iniative = checkLenAndCompareNumber(
                'iniative', data['iniative'], error)
            finalNote = checkLenOfField(
                'finalNote', data['finalNote'], 1, error)
            userId = checkLenOfField('userId', data['userId'], 1, error)
            profileUser = checkLenOfField(
                'profileUser', data['profileUser'], 1, error)
            decision = checkLenOfField(
                'decision', data['trueRadio'], 1, error)
            comment = checkLenOfField('comment', data['comment'], 10, error)

            if error:
                for data in error:
                    for dat in data:
                        errors[dat] = data[dat]
            if len(error) == 0 and len(errors) == 0:
                evaluation = EvaluationFile.objects.create(user_id=int(userId), profileUser_id=int(profileUser), punctuation=int(punctuality),
                                                           adaptation=int(adaptation), respect=int(respect), iniative=int(iniative), finalNote=int(finalNote), decision=decision, comments=comment)
                evaluation.save()
                return Response('success', status=status.HTTP_200_OK)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
