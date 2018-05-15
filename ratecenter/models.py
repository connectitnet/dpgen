from django.db import models

# Create your models here.
class Ratecenter(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    region = models.ForeignKey('Region')

class Region(models.Model):
    name = models.CharField(max_length=50)