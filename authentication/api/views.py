from django.db import transaction
from administration.utils import id_generator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from professionalHouse.regex import *
from authentication.models import *
from rest_framework.response import Response
from rest_framework import status
from authentication.models import *
from authentication.api.serializers import *
from django.contrib.auth import authenticate, login, logout
import jwt
import datetime


class UserAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all().order_by('-updated')
        serializers = UserSerializers(users, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class LoginView(APIView):

    def post(Self, request):
        errors = {}
        data = JSONParser().parse(request)
        email = data['email']
        password = data['password']

        userr = authenticate(request, email=email, password=password)

        user = User.objects.filter(email=email)

        if user is None or not user.exists():
            errors["email"] = "Cet utilisateur n'existe pas"
        if user.exists() and userr == None:
            errors["password"] = "Mot de passe incorrect"

        if len(errors) == 0:
            user = User.objects.get(email=email)
            payload = {
                'id': user.id,
                'role': user.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
                'key': 'archiSoftware'
            }

            token = jwt.encode(payload, 'secret',
                               algorithm='HS256').decode('utf-8')
            login(request, userr)

            response = Response()
            response.set_cookie(key='token', value=token, httponly=True)
            response.data = {'token': token, "id": user.id}
            return response
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    serializer_class = UserSerializers

    @transaction.atomic
    def post(self, request):
        if request.method == "POST":
            data = request.POST
            error = []
            errors = {}
            name = checkLenOfField('name', data['name'], 2, error)
            surname = checkLenOfField('surname', data['surname'], 1, error)
            city = checkLenOfField('cityLive', data['cityLive'], 1, error)
            email = setEmailError('email', data['email'], error)
            role = checkLenOfField('typeUser', data['typeUser'], 2, error)
            phone = checkIfNumber(data['phone'], 'phone', error)
            password1 = checkLenOfField(
                'password1', data['password1'], 2, error)
            password2 = checkLenOfField(
                'password2', data['password2'], 2, error)

            if password1 != password2:
                errors['password2'] = "Les mots de passe ne correspondent"
            else:
                pass

            emai = User.objects.filter(email=email)
            if emai.exists():
                errors['email'] = 'Cet adresse email existe déja'
            else:
                pass

            for data in error:
                for dat in data:
                    errors[dat] = data[dat]

            if len(errors) == 0 and len(error) == 0:
                username = name + id_generator()
                user = User.objects.create_user(username=username, name=name, surname=surname, email=email, password=password1,
                                                phone=phone, city=city, role=role)
                user.save()
                serializer = UserSerializers(user)
                return Response('user created', status=status.HTTP_201_CREATED)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
