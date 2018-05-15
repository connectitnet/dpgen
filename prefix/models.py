from django.db import models

# Create your models here.

class NPANXX(models.Model):
    npa = models.CharField(max_length=3)
    nxx = models.CharField(max_length=3)
    rate_center = models.ForeignKey('ratecenter.Ratecenter')
    manual_entry = models.BooleanField(editable=False, default=True)
    local_to = models.ManyToManyField('self', through='NPANXXThrough')

class NPANXXThrough(models.Model):
    npanxx_from = models.ForeignKey('NPANXX', related_name='from')
    npanxx_to = models.ForeignKey('NPANXX', related_name='to')
