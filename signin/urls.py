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

    path('graph/', views.graph_events_page, name='graph'),
    path('graph_people/', views.graph_people_page, name='graph_people'),

    path('options/', views.options_page, name='options'),

    path('api/signin', views.SignInHandler.as_view(), name='signin_request'),

    path('api/graph_events/', views.GraphEventsHandler.as_view(), name='graph_events_request'),
    path('api/graph_people/', views.GraphPeopleHandler.as_view(), name='graph_people_request'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
