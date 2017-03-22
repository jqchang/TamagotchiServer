from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Berry, Player, Batch

# Create your views here.
def index(request):
    # Batch.objects.checkExpiry(request.POST)
    return render(request, 'mapserver/index.html')

def apiList(request):
    lastbatch = Batch.objects.checkExpiry(request.POST)
    berrylist = lastbatch.berries.all().values('id', 'longitude', 'latitude', 'color')
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
