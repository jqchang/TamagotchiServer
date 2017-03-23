from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime, tzinfo, timedelta
from math import sin, cos, sqrt, atan2, radians
import random
import re

# Create your models here.
def haversine(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    dlon = float(lon2) - float(lon1)
    dlat = float(lat2) - float(lat1)

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

class BatchManager(models.Manager):
    def checkExpiry(self, postData):
        if len(Batch.objects.all()) == 0:
            newBatch = Batch.objects.create()
        if len(Batch.objects.order_by("-created_at")[0].berries.all()) == 0 or timezone.now() - Batch.objects.order_by("-created_at")[0].created_at > timedelta(hours=2):
            # If no batches exist - create new Batch
            print "new batch at {}".format(timezone.now() - Batch.objects.order_by("-created_at")[0].created_at)
            newBatch = Batch.objects.create()
            for _ in range(0,30):
                x = 37.3748851 + (random.random() * random.choice([-0.1, 0.1]))
                y = -121.911194 + (random.random() * random.choice([-0.1, 0.1]))
                color = random.choice(range(0,4))
                newBerry = Berry.objects.create(longitude=x, latitude=y, color=color, batch=newBatch)
        return Batch.objects.order_by("-created_at")[0]


class PlayerManager(models.Manager):
    def validate(self, postData):
        errors = []
        username = postData["player_name"]
        if len(username) < 3:
            errors.append("Name must be 3 or more characters.")
        if not re.search("^[A-Za-z0-9_-]*$", username):
            errors.append("Name can only contain letters, numbers, dash, or underscore.")
        if len(Player.objects.filter(username=player_name)) > 0:
            errors.append("Name is already taken.")
        if len(errors) == 0:
            return {"success":True, "playerObject": Player.objects.create()}
        else:
            return {"success":False, "errorList":errors}


class BerryManager(models.Manager):
    def pickup(self, postData):
        playerID = postData["playerID"]
        playerLong = postData["playerLong"]
        playerLat = postData["playerLat"]
        berryID = postData["berryID"]
        try:
            target = Berry.objects.get(id=berryID)
        except Berry.DoesNotExist:
            return {"success":False, "error":"Berry not found."}
        try:
            picker = Player.objects.get(id=playerID)
        except Player.DoesNotExist:
            return {"success":False, "error":"Player not found."}

        print(haversine(playerLat, playerLong, target.latitude, target.longitude))
        if haversine(playerLat, playerLong, target.latitude, target.longitude) < 0.01:
            target.pickedBy.add(picker)
            if target.pickedBy.values('id').distinct().count() >= 3:
                target.delete()
            else:
                return {"success":False, "error":"Berry has already been picked."}
        else:
            return {"success":False, "error":"Berry not in range."}
        picked = Berry.pickedBy.all()
        if picked.filter(id=int(playerID)):
            return {"success":False, "error":"You have already picked that berry."}


class Player(models.Model):
    username = models.CharField(max_length=45)
    last_request = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PlayerManager()


class Batch(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BatchManager()


class Berry(models.Model):
    longitude = models.DecimalField(decimal_places=5, max_digits=8)
    latitude = models.DecimalField(decimal_places=5, max_digits=8)
    pickedBy = models.ManyToManyField(Player, related_name="hasPicked")
    color = models.IntegerField(default=0)
    batch = models.ForeignKey(Batch, related_name="berries", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BerryManager()
