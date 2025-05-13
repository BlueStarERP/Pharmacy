from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from .forms import *
from django.db.models import Sum, F
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'base.html')

@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('name')
    return render(request, 'customer_list.html', {'customers': customers})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    prescriptions = Prescription.objects.filter(customer=customer).order_by('-prescription_date')
    sales = Sale.objects.filter(customer=customer).order_by('-created_at')
    return render(request, 'customer_detail.html', {
        'customer': customer,
        'prescriptions': prescriptions,
        'sales': sales
    })