from django.urls import path
from . import views



urlpatterns = [
    path('',views.index , name='index'),
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('device/', views.deviceController, name='device'),
    path('data/',views.data, name='data'),
]