from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.signin_page, name='signin'),
    path('signout/', views.signout_page, name='signout')
]
