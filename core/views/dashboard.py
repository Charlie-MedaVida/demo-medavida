from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.state import token_backend
from ..serializers import UserSerializer


from pprint import pprint


BEARER_TOKEN_PREFIX = 'Bearer '


class DashboardRetrieveAPIView(generics.RetrieveAPIView):
    name = 'DashboardRetrieveAPIView'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, **kwargs):
        # Parse JWT
        pprint(request.META)
        received_token = request.META.get('HTTP_AUTHORIZATION')
        token = received_token.replace(BEARER_TOKEN_PREFIX, '')
        token_payload = token_backend.decode(token, verify=True)
        current_user_id = token_payload['user_id']
        current_user = User.objects.get(
            id=current_user_id
        )
        serializer = UserSerializer(current_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
