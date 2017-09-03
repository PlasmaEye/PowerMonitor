# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Meter(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    type = models.IntegerField(default=0)

class Reading(models.Model):    
    consumption = models.IntegerField(default=0)
    time = models.DateTimeField()
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
