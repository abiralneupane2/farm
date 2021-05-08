from django.shortcuts import render, redirect
from django.views import View
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms import formset_factory
from . import models, forms, tables
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def index(request):
    user = request.user
    device = user.employee.farm.device
    readings = device.get_all_readings
    if request.method == POST:
        pass
    return render(request, 'index.html', {'readings': readings})



def deviceController(request):
    device = request.user.employee.farm.device
    if request.method=='POST':
        sqs=device.get_all_switches
        rqs=device.get_all_readings
        sformset = modelformset_factory(models.Switch,form=forms.SwitchForm, extra=0)
        msformset = sformset(request.POST, queryset=sqs)
        rformset = modelformset_factory(models.Reading,form=forms.ReadingForm, extra=0)
        mrformset = rformset(request.POST, queryset=rqs)
        if msformset.is_valid():
            msformset.save()
        else:
            print("msformset")
        if mrformset.is_valid():
            mrformset.save()
                
            # return render(request, 'device.html', {'sform': msformset, 'rform': mrformset,})
        else:
            print('not valid')
    
    
    sqs=device.get_all_switches
    rqs=device.get_all_readings
    sformset=modelformset_factory(models.Switch, form=forms.SwitchForm, extra=0)
    rformset=modelformset_factory(models.Reading, form=forms.ReadingForm, extra=0)
    msformset = sformset(queryset=sqs)
    mrformset = rformset(queryset=rqs)
    context={
        'sform': msformset,
        'rform': mrformset,
    }
    return render(request, 'device.html', context)
    # sformset=inlineformset_factory(models.Device, models.Switch, exclude=['device'])
    # rformset=inlineformset_factory(models.Device, models.Reading, exclude=['device'])
    # msformset = sformset(request.POST, instance=device)
    # mrformset = rformset(request.POST, instance=device)

    
            

    
    
    
    
    


class InventoryView(View):
    def get(self, request):
        farm = request.user.employee.farm
        context = {
            'medicinetable': tables.MedicineTable(farm.get_all_medicines),
            'foodtable': tables.FoodTable(farm.get_all_food),
            'eggs': farm.get_all_eggs,
            'medicineform': forms.MedicineForm(),
            'foodform': forms.FoodForm()
            # 'chicken': farm.get_all_chicken
        }
        return render(request, 'inventory.html', context)
    def post(self, request):
        farm = request.user.employee.farm
        medicineForm = forms.MedicineForm(request.POST)
        foodForm = forms.FoodForm(request.POST)
        if medicineForm.is_valid():
            addItem(request, medicineForm, models.Medicine, farm)
        elif foodForm.is_valid():
            addItem(request, foodForm, models.Food, farm)
        else:
            return redirect(reverse('inventory'))
        context = {
            'medicinetable': tables.MedicineTable(farm.get_all_medicines),
            'foodtable': tables.FoodTable(farm.get_all_food),
            'eggs': farm.get_all_eggs,
            'medicineform': forms.MedicineForm(),
            'foodform': forms.FoodForm()
            # 'chicken': farm.get_all_chicken
        }
        return render(request, 'inventory.html', context)

def addItem(request, myform, mymodel, farm):
    try:
        temp = mymodel.objects.get(name=request.POST.get('name'))
        mform = myform.__init__(request.POST, instance=temp)
        mform.save()
    except:
        mform = myform.__init__(request.POST)
        temp = myform.save(commit=False)
        temp.farm = farm
        temp.save()
    return 

@csrf_exempt
def data(request):
    if request.method=='POST':
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        id = request.POST.get('id')
        mdevice = models.Device.objects.get(id=id)
        mreading = models.Reading.objects.get(name='temperature')
        models.Data(reading=mreading, value=temperature).save()
        mreading = models.Reading.objects.get(name='humidity')
        models.Data(reading=mreading, value=temperature).save()
        return HttpResponse(status=200)