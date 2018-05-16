from django.db import models
from django.db.models import PROTECT

class Exchange(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    number = models.PositiveIntegerField()
    region = models.ForeignKey('prefix.Region', on_delete=PROTECT)

