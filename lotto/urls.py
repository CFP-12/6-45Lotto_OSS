from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('results/', views.check_results, name='check_results'),
]