from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.state import token_backend
from ..serializers import UserSerializer, UserDeleteSerializer

BEARER_TOKEN_PREFIX = 'Bearer '


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    name = 'USER_RETRIEVE_UPDATE_DESTROY'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, **kwargs):
        print(request.user.api_keys)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        # Parse JWT and obtaining user
        received_token = request.META.get('HTTP_AUTHORIZATION')
        token = received_token.replace(BEARER_TOKEN_PREFIX, '')
        token_payload = token_backend.decode(token, verify=True)
        current_user_id = token_payload['user_id']

        # Obtaining user
        current_user = User.objects.get(
            id=current_user_id
        )

        # Obtaining data information
        data = request.data.copy()
        # Validating data serializer
        serializer = UserSerializer(current_user, data=data, partial=True)

        # Updating objetc after serializer validation
        serializer.is_valid(raise_exception=True)
        current_user = serializer.save()

        serializer_response = UserSerializer(current_user)
        return Response(serializer_response.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        received_token = request.META.get('HTTP_AUTHORIZATION')
        token = received_token.replace(BEARER_TOKEN_PREFIX, '')
        token_payload = token_backend.decode(token, verify=True)
        current_user_id = token_payload['user_id']

        data = dict()
        data['user_id'] = current_user_id
        serializer = UserDeleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=data['user_id'])
        user.delete()

        return Response({"message": "User Deleted"}, status=status.HTTP_200_OK)
