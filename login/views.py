from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404 # JsonResponse and HttpResponseRedirect may be used in other APIs
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import User
import json
import requests
import base64
import urllib

CLIENT_ID = 'Iv1.4ecad6f945b81b88'
CLIENT_SECRET = 'ae2f1ce01433b0e49f33ba35c2a13a4f3a83abc8'

TWITTER_CLIENT_ID = 'UGxoMHJDc0JFcWNvMzkxeDZjMEk6MTpjaQ'
TWITTER_CLIENT_SECRET = 'sE1SZ6JRbu0694bhjSVZGdwPgZLD-V_FLoSu3-Zt-13h0MCIqD'

# Create your views here.
@require_http_methods(['GET'])
def index(request):
    return HttpResponse("Successfully connected to the github_login view.")

@require_http_methods(['GET'])
def github_login(request):
    print("request", request)
    # return HttpResponse("Successfully connected to the github_login view.")

# POST github_login
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def github_login(request):

    # print("request", request)
    # ############# GET ############# #
    if request.method == 'GET':
        print("request", request.GET['code'])
    
        try:
            code = request.GET['code']
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
        # print("res.text", text)
        access_token = text.split('&')[0].split('=')[1]
        # print("access_token", access_token)
        
        response = requests.get('https://api.github.com/user',headers={'Authorization':'Bearer '+access_token}) 
        if response.status_code != 200:
            # raise Http404("code is expired , please try to login again")
            return HttpResponse("code is expired , please try to login again",status=404)
        res_data = response.json()
        # print("res_data", res_data)
        
        username = res_data['login']
        email = res_data['email']  # some users make their email private so you might get none sometimes

        try:
            user = User.objects.get(username = username)
            return JsonResponse({"token":access_token, "data":username})
            # return HttpResponse("Welcome back '%s'." % access_token)
        except User.DoesNotExist:
            # Write the data to the database
            data_time_created = timezone.now()
            new_user = User.objects.create(username = username, creation_time = data_time_created)
            return HttpResponse("Welcome, %s! You have created an account at %s." % (new_user.username, new_user.creation_time))
        
        # return JsonResponse({"token":"token"})
    
    # ############# POST ############# #

    elif request.method == 'POST':
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
        # print("res.text", text)
        access_token = text.split('&')[0].split('=')[1]
        # print("access_token", access_token)
        
        response = requests.get('https://api.github.com/user',headers={'Authorization':'Bearer '+access_token}) 
        if response.status_code != 200:
            # raise Http404("code is expired , please try to login again")
            return HttpResponse("code is expired , please try to login again",status=404)
        res_data = response.json()
        # print("res_data", res_data)
        
        username = res_data['login']
        email = res_data['email']  # some users make their email private so you might get none sometimes

        try:
            user = User.objects.get(username = username)
            return JsonResponse({"token":access_token, "data":username})
            # return HttpResponse("Welcome back '%s'." % access_token)
        except User.DoesNotExist:
            # Write the data to the database
            data_time_created = timezone.now()
            new_user = User.objects.create(username = username, creation_time = data_time_created)
            return HttpResponse("Welcome, %s! You have created an account at %s." % (new_user.username, new_user.creation_time))
        
        # return JsonResponse({"token":"token"})

@require_http_methods(['POST'])
@csrf_exempt
def twitter_login(request):
    try:
        code = json.loads(request.body).get("code")
    except:
        raise Http404("you need to provide code in your post request")

    TWITTER_OAUTH_TOKEN_URL = "https://api.twitter.com/2/oauth2/token"

    message = f'{TWITTER_CLIENT_ID}:{TWITTER_CLIENT_SECRET}'
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    BasicAuthToken = base64_bytes.decode('utf-8')
    
    data = dict()
    data['client_id'] = urllib.parse.quote(TWITTER_CLIENT_ID)
    data['code_verifier'] = urllib.parse.quote("challenge")
    data['redirect_uri'] = "http://localhost:8080/login"
    data['grant_type'] = urllib.parse.quote("authorization_code")
    data['code'] = urllib.parse.quote(code)

    res = requests.post(TWITTER_OAUTH_TOKEN_URL,data,
            headers={
                'Authorization':'Basic '+BasicAuthToken,
                "Content-Type": "application/x-www-form-urlencoded"
        })
    
    if res.status_code == 200:
        data = res.json()
        return JsonResponse({"token":data["access_token"]})
    

    return HttpResponse("Something went wrong , please try to login again",status=404)

@require_http_methods(['POST'])
@csrf_exempt
def tweet(request):
    try:
        data = json.loads(request.body)
        text = data.get("text")
        accessToken = data.get("token")
    except:
        raise Http404("you need to provide text and accessToken in your post request")

    data = {
        "text":text
    }
    # print(data)
    # print(accessToken)
    
    res = requests.post(
        'https://api.twitter.com/2/tweets',json=data,headers={'Authorization':'Bearer '+accessToken,"Content-Type": "application/json"}
    )
    print(res.status_code,res.text)
    if res.status_code == 201:
        return HttpResponse("your tweet is submitted successfully")
    elif res.status_code == 403:
        return HttpResponse("Wrong token or expired , please try to login again",status=403)

    return HttpResponse("Something went wrong , please try to login again",status=404)