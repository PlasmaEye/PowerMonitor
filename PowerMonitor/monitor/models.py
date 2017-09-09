# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Meter(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    type = models.IntegerField(default=0)

    electric_types = {4, 5, 7, 8}
    gas_types = {2, 9, 12}
    water_types = {11, 13}

    def type_description(self):
        "Returns the description of the type."
        if(self.type in self.electric_types):
            return 'Electric'
        elif(self.type in self.gas_types):
            return 'Gas'
        elif(self.type in self.water_types):
            return 'Water'
        else:
            return 'Unknown'

class Reading(models.Model):    
    consumption = models.IntegerField(default=0)
    time = models.DateTimeField()
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
