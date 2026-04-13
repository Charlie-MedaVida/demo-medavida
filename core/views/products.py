from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import StripePrice
from ..serializers.stripe import StripePriceSerializer


class ProductListAPIView(generics.ListAPIView):
    name = 'ProductListAPIView'
    queryset = StripePrice.objects.all()
    serializer_class = StripePriceSerializer
    permission_classes = [IsAuthenticated]
