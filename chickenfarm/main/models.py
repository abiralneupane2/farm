from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db import models

STATUS = [
    ('U', 'Used'),
    ('A', 'Added')
]

GENDER = [
    ('M', 'Male'),
    ('F', 'Female')
]



class Farm(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name
    @property
    def get_all_medicines(self):
        return Medicine.objects.filter(farm=self)

    @property
    def get_all_food(self):
        return Food.objects.filter(farm=self)

    @property
    def get_all_eggs(self):
        return Egg.objects.filter(farm=self)




class Device(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=19, null=True)
    wifi_ssid = models.CharField(max_length=20, null=True)
    wifi_password = models.CharField(max_length=20, null=True   )

    @property
    def get_all_switches(self):
        return Switch.objects.filter(device=self)

    @property
    def get_all_readings(self):
        return Reading.objects.filter(device=self)

    

    def __str__(self):
        return self.farm.name

class Reading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='test', unique=True)
    description = models.CharField(max_length=100)

    def get_few_data(self):
        return Data.objects.filter(reading=self).order_by('-id')[:10][::-1]
    def __str__(self):
        return f'{self.device.farm.name}:{self.name}'

class Data(models.Model):
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f'{self.reading.name}: {self.value}'

class Switch(models.Model):
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='test')
    value = models.BooleanField()
    comment = models.CharField(max_length=100)

    

    def __str__(self):
        return f'{self.name}: {self.value}'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Budget(models.Model):
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    def __str__(self):
        return self.amount


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100, default='dana')
    quantity = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'



class Water(models.Model):
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.timestamp



class Chicken(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now=True)
    gender = models.CharField(choices=GENDER, max_length=1)

    def __str__(self):
        return f'{self.farm}, {self.id}'


class Egg(models.Model):
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(Chicken, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

class Log(models.Model):
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=10)