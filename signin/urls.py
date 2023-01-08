from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'signin'
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin_page, name='signin'),
    path('signout/', views.signout_page, name='signout'),
    path('qrsignin/', views.qr_signin_page, name='qrsignin'),
    path('qrsignout/', views.qr_signout_page, name='qrsignout'),
    path('generateqr/', views.generate_qr_page, name='generateqr'),
    path('graph/', views.graph_page, name='graph'),
    path('api/signin', views.signin_request, name='signin_request'),
    path('api/graph', views.graph_request, name='graph_request')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
