from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from practices.models import Practice
from ..serializers.auth import (
    SignupSerializer,
    OrigTokenObtainPairSerializer,
    OrigTokenBlockRefreshSerializer
)


BEARER_TOKEN_PREFIX = 'Bearer '


@permission_classes((AllowAny, ))
class SignInView(TokenObtainPairView):
    name = 'SIGN_IN'
    serializer_class = OrigTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['username'] = data['email']
        tokens = OrigTokenObtainPairSerializer(data).validate(data)
        return Response(tokens, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class SignUpView(generics.CreateAPIView):
    name = 'SIGN_UP'
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['username'] = data['email']
        serializer = SignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.create_user(
                serializer.initial_data['email'],
                password=serializer.initial_data['password'],
                email=serializer.initial_data['email'],
                first_name=serializer.initial_data['firstName'],
                last_name=serializer.initial_data['lastName'],
            )
        except IntegrityError:
            return Response(
                {'message': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        practice = Practice.objects.create(
            name=f"{serializer.initial_data['firstName']} {serializer.initial_data['lastName']}",
            email=serializer.initial_data['email'],
        )

        user.profile.practice = practice
        user.profile.save()

        tokens = OrigTokenObtainPairSerializer(data).validate(data)
        return Response(tokens, status=status.HTTP_201_CREATED)


@permission_classes((IsAuthenticated, ))
class SignOutView(ObtainAuthToken):
    name = 'SIGN_OUT'
    serializer_class = OrigTokenBlockRefreshSerializer

    def post(self, request, *args, **kwargs):
        response_message = OrigTokenBlockRefreshSerializer(request.data).validate(request.data)
        return Response({response_message}, status=status.HTTP_201_CREATED)
