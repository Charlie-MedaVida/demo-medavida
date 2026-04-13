from django.urls import path
from ..views import auth


app_name = 'auth'


urlpatterns = [
    path(
        'signin',
        auth.SignInView.as_view(),
        name=auth.SignInView.name
    ),
    path(
        'signup',
        auth.SignUpView.as_view(),
        name=auth.SignUpView.name
    ),
    path(
        'signout',
        auth.SignOutView.as_view(),
        name=auth.SignOutView.name
    ),
]
