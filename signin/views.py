import json
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Person, Signin


def index(request):
    return HttpResponseRedirect(reverse('signin:qrsignin'))


def get_signedin_people(signed_in: bool):
    # signed_in determines if it gets signed in people (True) or signed out people (False)
    people = {}     # dict with pk as key and name as value
    for person in Person.objects.all():
        if person.signin_set.count() == 0:
            # if a person has no sign ins, treat them as signed out
            if not signed_in:
                people[person.pk] = person.name
        else:
            last_signin = person.signin_set.latest("date")  # gets the most recent sign in/out
            if last_signin.is_signin == signed_in:
                people[person.pk] = person.name
    return people


@staff_member_required
def signin_page(request):
    context = {"page": "signin", "is_signin": True}
    return render(request, 'signin/signin.html', context)


@staff_member_required
def signout_page(request):
    context = {"page": "signout", "is_signin": False}
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
    context = {"page": "generateqr"}
    return render(request, 'signin/generateqr.html', context)


@staff_member_required
def signin_request(request):    # this also handles signout requests
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            person = Person.objects.get(pk=data['pk'])
        except Person.DoesNotExist:
            return JsonResponse({"success": "false"})
        signin = Signin(is_signin=data['is_signin'], person=person)
        signin.save()
        return JsonResponse({"success": "true", "person": person.name})
