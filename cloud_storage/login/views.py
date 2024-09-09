from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .__init__ import supabase
from gotrue.errors import AuthApiError, AuthInvalidCredentialsError, AuthError
import json

def loginpage(request):
    return render(request, 'login.html', context={'action': 'login', 'signorlog': "Log in:"})


def signup(request):
    return render(request, 'login.html', context={'action': 'signing', 'signorlog': "Sign up:", "note": "It seems you're not our user yet. Please, sign in. If you are our user, there might've been a typo"})


def signing(request):
    supabase.auth.sign_up({'email':request.POST['Email'], 'password': request.POST['Password']})
    return HttpResponseRedirect("/loggedin/")

def login(request):
    try:
        supabase.auth.sign_in_with_password({'email': request.POST['Email'], 'password': request.POST['Password']})

    except AuthApiError:
        return HttpResponseRedirect('/signup/')

    except AuthInvalidCredentialsError:
        raise AuthInvalidCredentialsError("Please enter valid credentials.")

    return HttpResponseRedirect("/loggedin/")

def loggedin(request):
    user = supabase.auth.get_user()
    if user:
        return HttpResponse("zalogowano jako {}".format(json.loads(user.model_dump_json())['user']['user_metadata']['email']))
    else:
        raise AuthError("Log in first, please.", "no_authorization")