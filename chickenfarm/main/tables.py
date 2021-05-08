import django_tables2 as tables
from . import models

class MedicineTable(tables.Table):
    class Meta:
        model = models.Medicine
        exclude = ('farm','id')


class FoodTable(tables.Table):
    class Meta:
        model = models.Food
        exclude = ('farm','id')