from django.urls import path
from .views import ShowView,CartAddView,CartDeleteView,CartUpdateView

app_name = 'cart'
urlpatterns = [
    path(r'show', ShowView.as_view(), name='show'),
    path(r'add', CartAddView.as_view(), name='add'),
    path(r'update', CartUpdateView.as_view(), name='update'),
    path(r'delete', CartDeleteView.as_view(), name='delete')
]