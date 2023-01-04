from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def signin_page(request):
    context = {"is_signin": True}
    return render(request, 'signin/signin.html', context)


@staff_member_required
def signout_page(request):
    context = {"is_signin": False}
    return render(request, 'signin/signin.html', context)
