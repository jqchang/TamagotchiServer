from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from .models import Berry, Player, Batch
from datetime import datetime
from decimal import Decimal

# Create your views here.
def index(request):
    # Batch.objects.checkExpiry(request.POST)
    return render(request, 'mapserver/index.html')
    # return JsonResponse(list(Berry.objects.all().values('id', 'longitude', 'latitude', 'color', 'batch')), safe=False)

def apiList(request):
    lastbatch = Batch.objects.checkExpiry(request.POST)
    berrylist = lastbatch.berries.all().annotate(Count("pickedBy", distinct=True)).values('id', 'longitude', 'latitude', 'color', 'pickedBy__count')
    return JsonResponse(list(berrylist), safe=False)

def login(request):
    if request.method != 'POST':
        return JsonResponse({"success":False, "errors":["Invalid login request. Please log in through the app."]}, safe=False)

def firstLogin(request):
    if request.method != 'POST':
        return JsonResponse({"success":False, "errors":["Invalid login request. Please log in through the app."]}, safe=False)
    else:
        playerValid = Player.objects.validate(request.POST)
        return JsonResponse(playerValid)

def pickup(request):
    if request.method != 'POST':
        print("pickup found invalid login")
        return JsonResponse({"success":False, "errors":["Invalid login request. Please log in through the app."]}, safe=False)
    else:
        playerID = 1
        playerLong = 37.40640
        playerLat = -121.88333
        berryID = 662
        context = {
            "playerID":playerID,
            "playerLong":playerLong,
            "playerLat":playerLat,
            "berryID":berryID
        }
        pickupValid = Berry.objects.pickup(context)
        return JsonResponse(pickupValid)

def debug(request):
    return render(request, 'mapserver/admin.html')
