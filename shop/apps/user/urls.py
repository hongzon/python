from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import RegisterView, LoginView, LogoutView,UserView,OrderView,AddressView

app_name = 'user'
urlpatterns = [
    path(r'register', RegisterView.as_view(), name='register'),
    path(r'login', LoginView.as_view(), name='login'),
    path(r'logout', LogoutView.as_view(), name='logout'),
    path(r'user', UserView.as_view(), name='user'),
    path(r'order/<int:page>', OrderView.as_view(), name='order'),
    path(r'address', AddressView.as_view(), name='address')
]
