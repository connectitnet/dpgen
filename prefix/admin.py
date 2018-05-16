from django.contrib import admin

# Register your models here.
from prefix.models import NPANXX


def fetch_local_to_npanxx(modeladmin, request, queryset):
    for npanxx in queryset:
        npanxx.fetch_local_to()
fetch_local_to_npanxx.short_description = "Fetch NPANXXes local to this NPANXX"

class NPANXXAdmin(admin.ModelAdmin):

    def npanxx(self):
        return str(self)

    def local_to(self):
        return self.local_to.count()

    list_display = (npanxx, 'npa', 'nxx', 'region', 'manual_entry', local_to)
    list_filter = ('npa', 'region', 'manual_entry')
    actions = [fetch_local_to_npanxx]


admin.site.register(NPANXX, NPANXXAdmin)