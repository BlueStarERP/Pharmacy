from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import *
from .forms import *
from django.db.models import Sum, F
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import TemplateView, View, CreateView, DetailView,FormView
from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
# ===================================================User Log In ===============================
class UserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('UserLoginView')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = ULoginForm
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data['password']
        usr = authenticate(username=username, password=password)

        if usr is not None:
            login(self.request, usr)

        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid user login!'})
        return super().form_valid(form)

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('UserLoginView')


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