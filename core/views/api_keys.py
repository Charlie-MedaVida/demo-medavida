from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.state import token_backend
from rest_framework.permissions import IsAuthenticated
from ..serializers import UserAPIKeySerializer
from ..models import UserAPIKey


BEARER_TOKEN_PREFIX = 'Bearer '


class ApiKeyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    name = 'ApiKeyRetrieveUpdateAPIView'
    queryset = UserAPIKey.objects.all()
    serializer_class = UserAPIKeySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, **kwargs):
        received_token = request.META.get('HTTP_AUTHORIZATION')
        token = received_token.replace(BEARER_TOKEN_PREFIX, '')
        token_payload = token_backend.decode(token, verify=True)
        current_user_id = token_payload['user_id']
        current_user = User.objects.get(id=current_user_id)
        api_key = UserAPIKey.objects.get(user=current_user)
        serializer = self.serializer_class(api_key)
        return Response(serializer.data, status=status.HTTP_200_OK)
