from django.urls import path

from . import views

app_name = 'signin'
urlpatterns = [
    path('signin/', views.qr_signin_page, name='signin'),
    path('signout/', views.qr_signout_page, name='signout'),
    path('qrsignin/', views.qr_signin_page, name='qrsignin'),
    path('qrsignout/', views.qr_signout_page, name='qrsignout'),
    path('api/signin', views.signin_request, name='signin_request')
]
