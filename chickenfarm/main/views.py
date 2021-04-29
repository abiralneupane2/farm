from django.shortcuts import render, redirect
from django.views import View
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms import formset_factory
from . import models, forms
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


def deviceController(request):
    device = request.user.employee.farm.device
    if request.method=='POST':
        sqs=device.get_all_switches
        rqs=device.get_all_readings
        sformset = modelformset_factory(models.Switch, form=forms.SwitchForm, extra=0)
        msformset = sformset(request.POST, queryset=sqs)
        print(request.POST)
        rformset = modelformset_factory(models.Reading, form=forms.ReadingForm, extra=0)
        mrformset = rformset(request.POST, queryset=rqs)
        if msformset.is_valid() and mrformset.is_valid():
            for sform in msformset:
                temp = sform.save(commit=False)
                temp.device=device
                temp.save()
            for rform in mrformset:
                temp = rform.save(commit=False)
                temp.device=device
                temp.save()
                
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
            'medicines': farm.get_all_medicines,
            'food': farm.get_all_food,
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
            'medicines': farm.get_all_medicines,
            'food': farm.get_all_food,
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