import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Person, Signin


@staff_member_required
def signin_page(request):
    context = {"is_signin": True}
    return render(request, 'signin/signin.html', context)


@staff_member_required
def signout_page(request):
    context = {"is_signin": False}
    return render(request, 'signin/signin.html', context)


@staff_member_required
def signin_request(request):    # this is also handles signout requests
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            person = Person.objects.get(pk=data['pk'])
        except Person.DoesNotExist:
            return JsonResponse({"success": "false"})
        signin = Signin(is_signin=data['is_signin'], person=person)
        signin.save()
        return JsonResponse({"success": "true", "person": person.name})
