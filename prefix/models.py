from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.db.models import PROTECT, CASCADE

from dpgen.utils import get_local_prefixes, get_npa_data, get_ranges_from_iterable


class NPANXX(models.Model):
    npa = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)],
        verbose_name="NPA"
    )
    nxx = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)],
        verbose_name="NXX"
    )
    manual_entry = models.BooleanField(editable=False, default=True)
    local_to = models.ManyToManyField('self', through='NPANXXIsLocal', symmetrical=False)
    region = models.ForeignKey('prefix.Region', on_delete=PROTECT, editable=False, blank=True)

    notes = models.TextField(blank=True)

    def fetch_local_to(self):
        prefixes = get_local_prefixes(npa=self.npa, nxx=self.nxx)
        for prefix in prefixes:
            npanxx, created = NPANXX.objects.get_or_create(
                npa=prefix['npa'], nxx=prefix['nxx'], defaults={'manual_entry': False}
            )
            NPANXXIsLocal.objects.get_or_create(npanxx_src=self, npanxx_dest=npanxx)
            NPANXXIsLocal.objects.get_or_create(npanxx_src=npanxx, npanxx_dest=self)

    @property
    def local_to_as_list(self):
        return [npanxx.npa*1000+npanxx.nxx for npanxx in self.local_to.order_by('npa', 'nxx')]

    @property
    def local_to_npa_list(self):
        return [npanxx['npa'] for npanxx in self.local_to.order_by('npa').values('npa').distinct()]

    def get_local_to_as_list_from_npa(self, npa):
        return [npanxx.nxx for npanxx in self.local_to.filter(npa=npa).order_by('nxx')]

    @property
    def local_to_prefixes_as_dict(self):
        return_data = dict()
        npa_list = self.local_to_npa_list
        for npa in npa_list:
            prefixes = self.get_local_to_as_list_from_npa(npa)
            return_data[npa] = get_ranges_from_iterable(prefixes)
        return return_data




    def save(self, *args, **kwargs):
        npa = get_npa_data(npa=self.npa)
        region, created = Region.objects.get_or_create(name=npa['region'], long_name=npa['rname'])
        self.region = region
        super().save(*args, **kwargs)

    def __str__(self):
        return "({npa}) {nxx}".format(npa=self.npa, nxx=self.nxx)

    class Meta:
        unique_together = (("npa", "nxx"),)
        verbose_name = 'NPANXX'
        verbose_name_plural = 'NPANXXes'


class NPANXXIsLocal(models.Model):
    npanxx_src = models.ForeignKey('prefix.NPANXX', related_name='dest_set', on_delete=CASCADE)
    npanxx_dest = models.ForeignKey('prefix.NPANXX', related_name='src_set', on_delete=CASCADE)
    manual_entry = models.BooleanField(editable=False, default=False)

    class Meta:
        unique_together = (('npanxx_src','npanxx_dest'),)


class Region(models.Model):
    name = models.CharField(max_length=50)
    long_name = models.CharField(max_length=50)

    def __str__(self):
        return self.long_name
