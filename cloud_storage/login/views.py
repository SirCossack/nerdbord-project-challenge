from django.shortcuts import render
from django.http import HttpResponseRedirect
from .__init__ import supabase
from gotrue.errors import AuthApiError, AuthInvalidCredentialsError
import json
import mimetypes


def loginpage(request):
    return render(request, 'login.html', context={'action': 'login', 'signorlog': "Log in:"})


def signup(request):
    return render(request, 'login.html', context={'action': 'signing', 'signorlog': "Sign up:", "note": "It seems you're not our user yet. Please, sign in. If you are our user, there might've been a typo"})


def signing(request):
    #Sessions covered with Supabase Auth
    try:
        supabase.auth.sign_up({'email': request.POST['Email'], 'password': request.POST['Password']})
        supabase.auth.sign_in_with_password(
            {'email': request.POST['Email'], 'password': request.POST['Password']})
    except (AuthInvalidCredentialsError, AuthApiError):
        return render(request, 'login.html', context={'action': 'signing', 'signorlog': "Sign up:",
                                                      "note": "Invalid credentials"})
    except Exception as e:
        return render(request, 'login.html', context={'action': 'signing', 'signorlog': "Sign up:", "note": str(e)})

    return HttpResponseRedirect("/loggedin/")


def login(request):
    #Sessions covered with Supabase Auth
    try:
        supabase.auth.sign_in_with_password({'email': request.POST['Email'], 'password': request.POST['Password']})
    except AuthApiError:
        return HttpResponseRedirect('/signup/')

    except AuthInvalidCredentialsError:
        return render(request, 'login.html', context={'action': 'login', 'signorlog': "Log in:", 'note': "Invalid credentials"})

    return HttpResponseRedirect("/loggedin/")


def loggedin(request):
    user = supabase.auth.get_user()
    if user:
        id = json.loads(user.model_dump_json())['user']['id']
        username = json.loads(supabase.auth.get_user().model_dump_json())['user']['user_metadata']['email']
        if request.FILES:
            try:
                file = request.FILES['uploadedfile']
                filename = file.name
                size = file.size
                print(size)
                if size > 5000000:
                    return render(request, "loggedin.html",
                                  context={'username': username, "filenote": "File too big"})
                mime_type, encoding = mimetypes.guess_type(filename)
                if mime_type.startswith('image/') or mime_type.startswith('text/'):
                    supabase.storage.from_('Files').upload('{}/{}'.format(id,filename), request.FILES['uploadedfile'].file.getbuffer().tobytes(),
                                                           {'content-type': '{}'.format(mime_type),})
                    return render(request, "loggedin.html", context={'username': username, "filenote": "File added successfully"})
                else:
                    return render(request, "loggedin.html",
                                  context={'username': username, "filenote": "Wrong file format"})
            except Exception as e:
                return render(request, "loggedin.html", context={'username': username, "filenote": "{}".format(e)})
        return render(request, "loggedin.html", context={'username': username})
    else:
        return HttpResponseRedirect("/")


def logout(request):
    user = supabase.auth.get_user()
    if user:
        supabase.auth.sign_out()
    return HttpResponseRedirect("/")
