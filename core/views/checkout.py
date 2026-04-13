import json
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from ..business_logic.users import set_subscription


ROOT = settings.FRONT_END_ROOT_URL


class CreateCheckoutView(APIView):
    name = 'CreateCheckoutView'

    def post(self, request, *args, **kwargs):
        lookup_key = request.data['lookup_key']
        try:
            stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
            prices = stripe.Price.list(
                lookup_keys=[lookup_key],
                expand=['data.product']
            )
            price_id = prices.data[0].id
            print(f"Price Id {price_id}")

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=ROOT + 'store/success?session_id={CHECKOUT_SESSION_ID}', # noqa
                cancel_url=ROOT + 'store/cancel',
                metadata={
                    'internal_user_id': request.user.id,
                    'lookup_key': lookup_key,
                },
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'sessionId': checkout_session.id,
            'url': checkout_session.url
        })


class CheckoutStatusRetrieveApiView(generics.RetrieveAPIView):
    name = 'CheckoutStatusRetrieveApiView'

    def retrieve(self, request, **kwargs):
        session_id = request.query_params['session_id']
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        return Response({
            'status': session.status,
            'customer_email': session.customer_details.email
        })


class CheckoutWebhookApiView(generics.CreateAPIView):
    name = 'CheckoutWebhookApiView'
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        event = None

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        if endpoint_secret:
            sig_header = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, endpoint_secret
                )
            except stripe.error.SignatureVerificationError as e:
                print('Webhook signature verification failed.' + str(e))
                return Response(
                    {'success': False},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if (
            event.type == 'checkout.session.completed' or
            event.type == 'checkout.session.async_payment_succeeded'
        ):
            checkout_session = event.data.object
            user_id = checkout_session.metadata['internal_user_id']
            lookup_key = checkout_session.metadata['lookup_key']
            set_subscription(user_id=user_id, lookup_key=lookup_key)
        else:
            print('Unhandled event type {}'.format(event.type))

        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )
