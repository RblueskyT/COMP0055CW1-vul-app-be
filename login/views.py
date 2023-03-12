from django.http import HttpResponse, JsonResponse, Http404 # JsonResponse and HttpResponseRedirect may be used in other APIs
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserStatus
from dashboard.models import Balance
from dashboard.models import BalanceRecord
import json
import requests
import base64
import urllib

# User login with account and password
@require_http_methods(['POST'])
@csrf_exempt
def account_login(request):
    username = json.loads(request.body).get("username")
    password = json.loads(request.body).get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        userState = UserStatus.objects.get(username=username)
        userState.isLoggedIn = True
        userState.save()
        return JsonResponse({"code": 200, "msg": "authentication succeeded"})
    else:
        return JsonResponse({"code": 403, "msg": "authentication failed"})

# Check if the user is authenticated
@require_http_methods(['POST'])
@csrf_exempt
def check_user_status(request):
    username = json.loads(request.body).get("username")
    try:
        user = User.objects.get(username=username)
        userState = UserStatus.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Unknown Error")
    if not userState.isLoggedIn:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if userState.isLoggedIn:
        return JsonResponse({"code": 200, "msg": "authentication succeeded"})
    
# Github login - redeem access token (client-flow)
@require_http_methods(['POST'])
@csrf_exempt
def github_client_flow_redeem(request):
    redeem_code = json.loads(request.body).get("code")
    gcfc_id = 'd83ac1ef7822f3087e4b'
    gcfc_secret = '8454a2f1e906f4816457d10ba1c662302db59491'
    data = {
        "client_id": gcfc_id,
        "client_secret": gcfc_secret,
        "code": redeem_code,
    }
    response = requests.post('https://github.com/login/oauth/access_token', data)
    if response.status_code != 200:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    else:
        return JsonResponse({"code": 200, "github_response": response.text})
    
# Github login - user login (client-flow)
@require_http_methods(['POST'])
@csrf_exempt
def github_client_flow_login(request):
    access_token = json.loads(request.body).get("access_token")
    response = requests.get('https://api.github.com/user',headers={'Authorization':'Bearer '+access_token})
    if response.status_code != 200:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    else:
        res_data = response.json()
        username = res_data['login'] + '(GitHub)'
        password = access_token
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                userState = UserStatus.objects.get(username=username)
                userState.isLoggedIn = True
                userState.save()
                return JsonResponse({"code": 200, "msg": 'authentication succeeded', "username": user.username})
            else:
                return JsonResponse({"code": 403, "msg": "authentication failed"})
        except User.DoesNotExist:
            newUser = User.objects.create_user(username, '', password)
            auth_new_user = authenticate(request, username=username, password=password)
            if auth_new_user is not None:
                new_balance = Balance.objects.create(username = username, current_balance = 150)
                new_balnce_record = BalanceRecord.objects.create(username = username, balance_change = 150, change_reason = 'account created', change_date = timezone.now(), balance = new_balance)
                login(request, auth_new_user)
                newUserState = UserStatus.objects.create(username = username, isLoggedIn = True)
                return JsonResponse({"code": 200, "msg": 'authentication succeeded', "username": newUser.username})
            else:
                return JsonResponse({"code": 403, "msg": "authentication failed"})
            
# Github login - return info (server-flow)
@require_http_methods(['GET'])
def github_server_flow_info(request):
    client_id = 'd83ac1ef7822f3087e4b'
    redirect_uri = 'http://localhost:8080/login'
    scope = 'user'
    return JsonResponse({"code": 200, "client_id": client_id, "redirect_uri": redirect_uri, "scope": scope})

# Github login - redeem access token and user login (server-flow)
@require_http_methods(['POST'])
@csrf_exempt
def github_server_flow_redeem_and_login(request):
    redeem_code = json.loads(request.body).get("code")
    gsfc_id = 'd83ac1ef7822f3087e4b'
    gsfc_secret = '8454a2f1e906f4816457d10ba1c662302db59491'
    data = {
        "client_id": gsfc_id,
        "client_secret": gsfc_secret,
        "code": redeem_code,
    }
    response = requests.post('https://github.com/login/oauth/access_token', data)
    if response.status_code != 200:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    elif 'bad_verification_code' in response.text:
        return JsonResponse({"code": 404, "msg": "bad verification code"})
    else:
        access_token = response.text.split('&')[0].split('=')[1]
        githubResponse = requests.get('https://api.github.com/user',headers={'Authorization':'Bearer '+access_token})
        if githubResponse.status_code != 200:
            return JsonResponse({"code": 403, "msg": "authentication failed"})
        else:
            res_data = githubResponse.json()
            username = res_data['login'] + '(GitHub)'
            password = access_token
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                auth_user = authenticate(request, username=username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    userState = UserStatus.objects.get(username=username)
                    userState.isLoggedIn = True
                    userState.save()
                    return JsonResponse({"code": 200, "msg": 'authentication succeeded', "username": user.username, "token": access_token})
                else:
                    return JsonResponse({"code": 403, "msg": "authentication failed"})
            except User.DoesNotExist:
                newUser = User.objects.create_user(username, '', password)
                auth_new_user = authenticate(request, username=username, password=password)
                if auth_new_user is not None:
                    new_balance = Balance.objects.create(username = username, current_balance = 150)
                    new_balnce_record = BalanceRecord.objects.create(username = username, balance_change = 150, change_reason = 'account created', change_date = timezone.now(), balance = new_balance)
                    login(request, auth_new_user)
                    newUserState = UserStatus.objects.create(username = username, isLoggedIn = True)
                    return JsonResponse({"code": 200, "msg": 'authentication succeeded', "username": newUser.username, "token": access_token})
                else:
                    return JsonResponse({"code": 403, "msg": "authentication failed"})
                
# Twitter login - return info (server-flow)
@require_http_methods(['GET'])
def twitter_server_flow_info(request):
    options = {
        "response_type": 'code',
        "client_id": 'UGxoMHJDc0JFcWNvMzkxeDZjMEk6MTpjaQ',
        "redirect_uri": 'http://localhost:8080/login',
        "state": 'state',
        "code_challenge": 'challenge',
        "code_challenge_method": 'plain',
        "scope": ' '.join(['users.read','tweet.write', 'tweet.read', 'follows.read', 'follows.write'])
    }
    return JsonResponse({"code": 200, "options": options})

# Twitter login - redeem access token and user login (server-flow)
@require_http_methods(['POST'])
@csrf_exempt
def twitter_server_flow_redeem_and_login(request):
    redeem_code = json.loads(request.body).get("code")
    tsfc_id = 'UGxoMHJDc0JFcWNvMzkxeDZjMEk6MTpjaQ'
    tsfc_secret = 'sE1SZ6JRbu0694bhjSVZGdwPgZLD-V_FLoSu3-Zt-13h0MCIqD'
    ba_token_raw = f'{tsfc_id}:{tsfc_secret}'
    ba_token_bytes = ba_token_raw.encode('utf-8')
    ba_token_base64 = base64.b64encode(ba_token_bytes)
    ba_token = ba_token_base64.decode('utf-8')

    data = {
        "client_id": urllib.parse.quote(tsfc_id),
        "code_verifier": urllib.parse.quote('challenge'),
        "redirect_uri": 'http://localhost:8080/login' ,
        "grant_type": urllib.parse.quote('authorization_code'),
        "code": urllib.parse.quote(redeem_code),
    }
    response = requests.post('https://api.twitter.com/2/oauth2/token', data, headers = {'Authorization':'Basic ' + ba_token, 'Content-Type': 'application/x-www-form-urlencoded'})
    if response.status_code != 200:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    else:
        resData = response.json()
        access_token = resData["access_token"]
        userInfoRes = requests.get('https://api.twitter.com/2/users/me', headers={'Authorization':'Bearer ' + access_token,"Content-Type": "application/json"})
        if response.status_code != 200:
            return JsonResponse({"code": 403, "msg": "authentication failed"})
        else:
            userInfo = userInfoRes.json()
            username = userInfo['data']['username'] + '(Twitter)'
            password = access_token
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                auth_user = authenticate(request, username=username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    userState = UserStatus.objects.get(username=username)
                    userState.isLoggedIn = True
                    userState.save()
                    return JsonResponse({"code": 200, "msg": 'authentication succeeded', "username": user.username, "token": access_token})
                else:
                    return JsonResponse({"code": 403, "msg": "authentication failed"})
            except User.DoesNotExist:
                newUser = User.objects.create_user(username, '', password)
                auth_new_user = authenticate(request, username=username, password=password)
                if auth_new_user is not None:
                    new_balance = Balance.objects.create(username = username, current_balance = 150)
                    new_balnce_record = BalanceRecord.objects.create(username = username, balance_change = 150, change_reason = 'account created', change_date = timezone.now(), balance = new_balance)
                    login(request, auth_new_user)
                    newUserState = UserStatus.objects.create(username = username, isLoggedIn = True)
                    return JsonResponse({"code": 200, "msg": 'authentication succeeded', "username": newUser.username, "token": access_token})
                else:
                    return JsonResponse({"code": 403, "msg": "authentication failed"})
                
# User logout
@require_http_methods(['POST'])
@csrf_exempt
def user_logout(request):
    username = json.loads(request.body).get("username")
    try:
        user = User.objects.get(username=username)
        userState = UserStatus.objects.get(username=username)
        userState = UserStatus.objects.get(username=username)
        userState.isLoggedIn = False
        userState.save()
        return HttpResponse("Successfully logged out")
    except User.DoesNotExist:
        raise Http404("Unknown Error")