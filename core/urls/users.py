from django.urls import path
from ..views import users
from ..views.dashboard import DashboardRetrieveAPIView


app_name = 'users'


urlpatterns = [
    path(
        'me',
        users.UserRetrieveUpdateDestroyView.as_view(),
        name=users.UserRetrieveUpdateDestroyView.name
    ),
    path(
        'me/dashboard',
        DashboardRetrieveAPIView.as_view(),
        name=DashboardRetrieveAPIView.name
    ),
]
