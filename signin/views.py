import json
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Person, Signin
from .graphing import graph_people


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
def graph_page(request):
    context = {"page": "graph", "people": get_people()}
    return render(request, 'signin/graph.html', context)


@staff_member_required
def signin_request(request):    # this also handles signout requests
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            person = Person.objects.get(pk=data['pk'])
        except (ValueError, Person.DoesNotExist):
            try:
                # if the getting someone by id doesn't work, try using their name (for legacy qr codes)
                person = Person.objects.get(name=data['pk'])
            except (ValueError, Person.DoesNotExist):
                return JsonResponse({"success": "false"})
        signin = Signin(is_signin=data['is_signin'], person=person)
        signin.save()
        return JsonResponse({"success": "true", "person": person.name})


@staff_member_required
def graph_request(request):
    data = json.loads(request.body)
    graph = graph_people(data['people_ids'])
    return JsonResponse({"graph": graph})
