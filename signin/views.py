import json
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Person, Session, Signin
from .graphing import graph_people, graph_events, get_last_event_num


def index(request):
    return HttpResponseRedirect(reverse('signin:signin'))


def get_people():
    people = {}
    for person in Person.people.all():
        people[person.pk] = person.name
    return people


def get_people_signin_status():
    # signed_in determines if it gets signed in people (True) or signed out people (False)
    people = {}     # dict with pk as key and name as value
    for person in Person.people.all():
        name = person.name
        if not person.media_permission:
            name += "﹒"

        if person.signin_set.count() == 0:
            # if a person has no sign ins, treat them as signed out
            people[person.pk] = {"name": name, "signed_in": False}
        else:
            last_signin = person.signin_set.latest("date")  # gets the most recent sign in/out
            people[person.pk] = {"name": name, "signed_in": last_signin.is_signin}
    return people


@staff_member_required
def signin_page(request):
    context = {"page": "signin", "is_signin": True, "people": get_people_signin_status()}
    return render(request, 'signin/signin.html', context)


@staff_member_required
def signout_page(request):
    context = {"page": "signout", "is_signin": False, "people": get_people_signin_status()}
    return render(request, 'signin/signin.html', context)


@staff_member_required
def qr_signin_page(request):
    context = {"page": "qrsignin", "is_signin": True}
    return render(request, 'signin/qrsignin.html', context)


@staff_member_required
def qr_signout_page(request):
    context = {"page": "qrsignout", "is_signin": False}
    return render(request, 'signin/qrsignin.html', context)


@staff_member_required
def generate_qr_page(request):
    context = {"page": "generateqr", "people": get_people()}
    return render(request, 'signin/generateqr.html', context)


@staff_member_required
def graph_events_page(request):
    context = {"page": "graph"}
    return render(request, 'signin/graph_events.html', context)


@staff_member_required
def graph_people_page(request):
    context = {"people": get_people()}
    return render(request, 'signin/graph_people.html', context)


@staff_member_required
def options_page(request):
    context = {"page": "options"}
    return render(request, 'signin/options.html', context)


class SignInHandler(APIView):
    """
    Handles Sign In/Out requests.
    """
    def post(self, request: Request):
        data = json.loads(request.body)

        try:
            person = Person.objects.get(pk=data['pk'])
            session = Session.objects.get(name=data['session'])
        except (ValueError, Person.DoesNotExist, Session.DoesNotExist):
            return JsonResponse({"success": "false"})

        signin = Signin(is_signin=data['is_signin'], person=person, session=session)
        signin.save()

        return JsonResponse({"success": "true", "person": person.name})


class GraphEventsHandler(APIView):
    def put(self, request: Request):
        events_graphs = graph_events()
        last_event = get_last_event_num()
        return JsonResponse({"events_graph": events_graphs, "last_event": last_event})


class GraphPeopleHandler(APIView):
    def put(self, request: Request):
        data = json.loads(request.body)
        people_graph = graph_people(data['people_ids'])
        return JsonResponse({"people_graph": people_graph})
