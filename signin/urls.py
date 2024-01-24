from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'signin'
urlpatterns = [
    path('', views.index, name='index'),

    path('signin/', views.signin_page, name='signin_default'),
    path('signin/<str:session>/', views.signin_page, name='signin_session'),

    path('graph/', views.graph_events_page, name='graph'),
    path('graph_people/', views.graph_people_page, name='graph_people'),

    path('spinner/', views.spinner_page, name='spinner'),

    path('options/', views.options_page, name='options'),

    path('api/signin/', views.SignInHandler.as_view(), name='api_signin'),

    path('api/graph_events/', views.GraphEventsHandler.as_view(), name='api_graph_events'),
    path('api/graph_people/', views.GraphPeopleHandler.as_view(), name='api_graph_people'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
