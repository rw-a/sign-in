from django.shortcuts import render


def signin_page(request):
    context = {"is_signin": True}
    return render(request, 'signin/signin.html', context)


def signout_page(request):
    context = {"is_signin": False}
    return render(request, 'signin/signin.html', context)
