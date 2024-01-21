import json
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Person, Session, Signin
from .graphing import graph_people, graph_events, get_last_event_num
from .sessions import get_default_session, get_people_signin_status, get_people_by_session, \
    is_sign_in_time


def index(request):
    return HttpResponseRedirect(reverse('signin:signin_default'))


@staff_member_required
def signin_page(request, *args, **kwargs):
    if "session" in kwargs:
        try:
            session = Session.objects.get(code=kwargs["session"].lower())
        except Session.DoesNotExist:
            return HttpResponseNotFound(f"Session '{kwargs['session']}' does not exist")

    else:
        # No session provided, so default to one (currently arbitrary)
        session = get_default_session()
        return HttpResponseRedirect(reverse('signin:signin_session', args=[session.code]))

    context = {
        "people": get_people_signin_status(session),
        "current_session": session,
        "all_sessions": Session.objects.all(),
        "is_sign_in_time": is_sign_in_time(session)
    }

    return render(request, 'signin/signin.html', context)


@staff_member_required
def graph_events_page(request):
    context = {
        "all_sessions": Session.objects.all(),
    }
    return render(request, 'signin/graph_events.html', context)


@staff_member_required
def graph_people_page(request):
    context = {
        "all_sessions": Session.objects.all(),
        "people_by_session": get_people_by_session()
    }
    return render(request, 'signin/graph_people.html', context)


@staff_member_required
def options_page(request):
    context = {
        "all_sessions": Session.objects.all(),
    }
    return render(request, 'signin/options.html', context)


class SignInHandler(APIView):
    """
    Handles Sign In/Out requests.
    """
    def post(self, request: Request):
        try:
            person = Person.objects.get(pk=request.data['pk'])
            session = Session.objects.get(code=request.data['session'])
        except (ValueError, Person.DoesNotExist, Session.DoesNotExist):
            return JsonResponse({"success": "false"})

        Signin.objects.create(
            is_signin=request.data['is_signin'],
            person=person,
            session=session
        )

        return JsonResponse({"success": "true", "person": person.name})


class GraphEventsHandler(APIView):
    def put(self, request: Request):
        session = Session.objects.get(code=request.data["session"])
        events_graphs = graph_events(session)
        last_event = get_last_event_num(session)
        return JsonResponse({"events_graph": events_graphs, "last_event": last_event})


class GraphPeopleHandler(APIView):
    def put(self, request: Request):
        session = Session.objects.get(code=request.data["session"])
        people_graph = graph_people(request.data['people_ids'], session)
        return JsonResponse({"people_graph": people_graph})
