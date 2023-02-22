from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404 # JsonResponse and HttpResponseRedirect may be used in other APIs
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import User
import json
import requests

CLIENT_ID = 'Iv1.4ecad6f945b81b88'
CLIENT_SECRET = 'ae2f1ce01433b0e49f33ba35c2a13a4f3a83abc8'

# Create your views here.
@require_http_methods(['GET'])
def index(request):
    return HttpResponse("Successfully connected to the github_login view.")

# POST github_login
@require_http_methods(['POST'])
@csrf_exempt
def github_login(request):
    try:
        code = json.loads(request.body).get("code")
    except:
        raise Http404("Unknown Error")

    data =  dict()
    data['client_id'] = CLIENT_ID
    data['client_secret'] = CLIENT_SECRET
    data['code'] = code
    
    res = requests.post('https://github.com/login/oauth/access_token',data)
    if res.status_code != 200:
        return HttpResponse("Wrong code , please try login again",status=404)
    text = res.text
    print("res.text", text)
    access_token = text.split('&')[0].split('=')[1]
    print("access_token", access_token)
    
    response = requests.get('https://api.github.com/user',headers={'Authorization':'Bearer '+access_token}) 
    if response.status_code != 200:
        # raise Http404("code is expired , please try to login again")
        return HttpResponse("code is expired , please try to login again",status=404)
    res_data = response.json()
    print("res_data", res_data)
    
    username = res_data['login']
    email = res_data['email']  # some users make their email private so you might get none sometimes

    try:
        user = User.objects.get(username = username)
        return JsonResponse({"token":access_token,
                             "data":username})
        # return HttpResponse("Welcome back '%s'." % user.username)
    except User.DoesNotExist:
        # Write the data to the database
        data_time_created = timezone.now()
        new_user = User.objects.create(username = username, creation_time = data_time_created)
        return HttpResponse("Welcome, %s! You have created an account at %s." % (new_user.username, new_user.creation_time))
    
    # return JsonResponse({"token":"token"})