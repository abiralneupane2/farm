from django.contrib import admin
from . import models, forms

from django.contrib.auth.models import User


# Register your models here.
@admin.register(models.Medicine)
class MedicineAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Employee)
admin.site.register(models.Farm)
admin.site.register(models.Switch)
admin.site.register(models.Reading)
@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    # form = forms.DeviceForm
    # fieldsets = (
    #     (None, {
    #         'fields': ('switch', 'value'),
    #     }),
    # )
    pass


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "timestamp")





