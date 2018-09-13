from django.urls import path

from . import views

urlpatterns = [
    path('subjects/', views.show_subjects,name='sub'),
    path('subjects/<int:no>', views.show_teachers,name='teachers'),
    path('good/<int:no>/', views.make_comment, name='good'),
    path('bad/<int:no>/', views.make_comment, name='bad'),
    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('check/',views.check_username, name='check'),
    path('logout/',views.logout, name='logout'),
]