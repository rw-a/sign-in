from django.urls import path

from . import views

app_name = 'signin'
urlpatterns = [
    path('signin/', views.signin_page, name='signin'),
    path('signout/', views.signout_page, name='signout'),
    path('api/signin', views.signin_request, name='signin_request')
]
