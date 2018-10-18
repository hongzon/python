from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'order'
urlpatterns = [
    path(r'place',OrderPlaceView.as_view(), name='place'),
    path(r'commit',OrderCommitView.as_view(), name='commit')
]
