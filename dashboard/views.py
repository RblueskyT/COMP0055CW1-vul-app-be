from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404 # JsonResponse and HttpResponseRedirect may be used in other APIs
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Balance
from .models import BalanceRecord
import json
import requests

# Get the balance of a user
@require_http_methods(['POST'])
@csrf_exempt
def get_user_balance(request):
    username = json.loads(request.body).get("username")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Unknown Error")
    if not user.is_authenticated:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if user.is_authenticated:
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
    if not user.is_authenticated:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if user.is_authenticated:
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
    if not src_user.is_authenticated:
        return JsonResponse({"code": 403, "msg": "authentication failed"})
    if src_user.is_authenticated:
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

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
