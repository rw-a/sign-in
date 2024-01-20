import json
from typing import TypedDict
from django.urls import reverse
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Person, Session, Signin
from .graphing import graph_people, graph_events, get_last_event_num


def index(request):
    return HttpResponseRedirect(reverse('signin:signin_default'))


def get_people():
    people = {}
    for person in Person.people.all():
        people[person.pk] = person.name
    return people


"""def get_sessions():
    pk = str

    class PersonType(TypedDict):
        name: str
        signed_in: bool

    class SessionType(TypedDict):
        is_signin: bool
        people: dict[pk, PersonType]

    sessions: list[SessionType] = []

    # For each active sessions (assume sign_in_time is always earliest)
    current_time = timezone.now()
    for session in Session.objects.all()\
            .filter(sign_in_time_lte=current_time)\
            .filter(end_time_gt=current_time)\
            .time():

        # True if it is time for people to be signing in (False if signing out)
        is_signin = current_time < session.sign_out_time

        # Get the people in the session
        # signed_in determines if it gets signed in people (True) or signed out people (False)
        people: dict[pk, PersonType] = {}
        for person in Person.people.all():
            name = person.name
            if not person.media_permission:
                name += "﹒"

            person_signins = person.signin_set.filter(session=session)

            if person_signins.count() == 0:
                # if a person has no sign ins, treat them as signed out
                people[person.pk] = {"name": name, "signed_in": False}
            else:
                last_signin = person_signins.latest("date")  # gets the most recent sign in/out
                people[person.pk] = {"name": name, "signed_in": last_signin.is_signin}

        sessions.append({"is_signin": is_signin, "people": people})

    return sessions"""


def get_people_signin_status(session: Session):
    # signed_in determines if it gets signed in people (True) or signed out people (False)
    people = {}     # dict with pk as key and name as value

    for person in Person.people.all():
        name = person.name
        if not person.media_permission:
            name += "﹒"

        person_signins = person.signin_set.filter(session=session)

        if person_signins.count() == 0:
            # if a person has no sign ins, treat them as signed out
            people[person.pk] = {"name": name, "signed_in": False}
        else:
            last_signin = person_signins.latest("date")  # gets the most recent sign in/out
            people[person.pk] = {"name": name, "signed_in": last_signin.is_signin}
    return people


"""def get_active_sessions():
    class SessionType(TypedDict):
        name: str
        is_signin: bool

    sessions: dict[str, SessionType] = {}

    current_time = timezone.now().time()
    for session in Session.objects.all() \
            .filter(sign_in_time_lte=current_time) \
            .filter(end_time_gt=current_time):

        # True if it is time for people to be signing in (False if signing out)
        is_signin = current_time < session.sign_out_time

        sessions[session.code] = {'name': session.name, 'is_signin': is_signin}

    return sessions"""


def get_active_sessions():
    current_time = timezone.now().time()

    return Session.objects.all()\
        .filter(sign_in_time__lte=current_time)\
        .filter(end_time__gt=current_time)


@staff_member_required
def signin_page(request, *args, **kwargs):
    if "session" in kwargs:
        try:
            session = Session.objects.get(code=kwargs["session"].lower())
        except Session.DoesNotExist:
            # TODO: Show a page listing possible sessions to redirect to
            return HttpResponseNotFound()

    else:
        # No session provided, so default to one (currently arbitrary)
        active_sessions = get_active_sessions()

        if len(active_sessions) > 0:
            session = active_sessions.latest("sign_in_time")
        else:
            session = Session.objects.all().latest("sign_in_time")

    people = get_people_signin_status(session)
    context = {
        "people": people,
        "current_session": session,
        "all_sessions": Session.objects.all()
    }

    return render(request, 'signin/signin.html', context)


@staff_member_required
def graph_events_page(request):
    return render(request, 'signin/graph_events.html')


@staff_member_required
def graph_people_page(request):
    context = {"people": get_people()}
    return render(request, 'signin/graph_people.html', context)


@staff_member_required
def options_page(request):
    return render(request, 'signin/options.html')


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
