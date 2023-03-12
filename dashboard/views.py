from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from login.models import UserStatus
from .models import Balance
from .models import BalanceRecord
from .models import Post
import json
import requests

@require_http_methods(['POST'])
@csrf_exempt
def tweet(request):
    username = json.loads(request.body).get("username")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Unknown Error")
    userState = UserStatus.objects.get(username=username)
    if not userState.isLoggedIn:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if userState.isLoggedIn:
        text = json.loads(request.body).get("text")
        accessToken = data.get("token")
        data = { "text": text }
        res = requests.post('https://api.twitter.com/2/tweets',json=data,headers={'Authorization':'Bearer '+accessToken,"Content-Type": "application/json"})
        if res.status_code == 201:
            return HttpResponse("your tweet is submitted successfully")
        elif res.status_code == 403:
            return HttpResponse("Wrong token or expired , please try to login again",status=403)
        return HttpResponse("Something went wrong , please try to login again",status=404)

# Get the balance of a user
@require_http_methods(['POST'])
@csrf_exempt
def get_user_balance(request):
    username = json.loads(request.body).get("username")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Unknown Error")
    userState = UserStatus.objects.get(username=username)
    if not userState.isLoggedIn:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if userState.isLoggedIn:
        userBalance = Balance.objects.get(username=username)
        return JsonResponse({"code": 200, "balance": userBalance.current_balance})
    
# Get the balance records a user
@require_http_methods(['POST'])
@csrf_exempt
def get_user_balance_records(request):
    username = json.loads(request.body).get("username")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Unknown Error")
    userState = UserStatus.objects.get(username=username)
    if not userState.isLoggedIn:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if userState.isLoggedIn:
        userBalanceRecords = BalanceRecord.objects.filter(username=username).values()
        userBalanceRecordsList = [record for record in userBalanceRecords]
        return JsonResponse({"code": 200, "balance_records": userBalanceRecordsList})

# Account transfer
@require_http_methods(['POST'])
@csrf_exempt
def account_transfer(request):
    src_username = json.loads(request.body).get("src_username")
    dst_username = json.loads(request.body).get("dst_username")
    amount = json.loads(request.body).get("amount")
    reason = json.loads(request.body).get("reason")
    try:
        src_user = User.objects.get(username=src_username)
        dst_user = User.objects.get(username=dst_username)
    except User.DoesNotExist:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    src_userState = UserStatus.objects.get(username=src_username)
    if not src_userState.isLoggedIn:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if src_userState.isLoggedIn:
        userBalanceOne = Balance.objects.get(username=src_username)
        userBalanceTwo = Balance.objects.get(username=dst_username)
        newBalanceOne = userBalanceOne.current_balance - amount
        nweBalanceTwo = userBalanceTwo.current_balance + amount
        userBalanceOne.current_balance = newBalanceOne
        userBalanceTwo.current_balance = nweBalanceTwo
        userBalanceOne.save()
        userBalanceTwo.save()
        new_balnce_record_one = BalanceRecord.objects.create(username = src_username, balance_change = -1*amount, change_reason = reason, change_date = timezone.now(), balance = userBalanceOne)
        new_balnce_record_two = BalanceRecord.objects.create(username = dst_username, balance_change = amount, change_reason = reason, change_date = timezone.now(), balance = userBalanceTwo)
        return JsonResponse({"code": 200, "msg": "Transfer Succeeded"})
    
# Get all posts
@require_http_methods(['POST'])
@csrf_exempt
def get_posts(request):
    username = json.loads(request.body).get("username")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    userState = UserStatus.objects.get(username=username)
    if not userState.isLoggedIn:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if userState.isLoggedIn:
        posts = Post.objects.all().values()
        postsList = [record for record in posts]
        return JsonResponse({"code": 200, "posts": postsList})
    
# Add a post
@require_http_methods(['POST'])
@csrf_exempt
def add_post(request):
    username = json.loads(request.body).get("username")
    post_title = json.loads(request.body).get("post_title")
    post_content = json.loads(request.body).get("post_content")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    userState = UserStatus.objects.get(username=username)
    if not userState.isLoggedIn:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if userState.isLoggedIn:
        new_post = Post.objects.create(username = username, post_title = post_title, post_content = post_content, post_date = timezone.now())
        return JsonResponse({"code": 200, "msg": "Post Creation Succeeded"})
