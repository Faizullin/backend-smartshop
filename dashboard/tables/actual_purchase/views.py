from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from shop_app.models import *
from .forms import *
from dashboard.decorators import group_required


@login_required()
@group_required(['shop-owner'])
def actual_purchase_index(request):
    actual_purchases = Purchase.objects.filter(status = "PENDING")
    context = {
        'segment': 'actual_purchase_index',
        'actual_purchases': actual_purchases,
        'form': PurchaseForm()
    }
    html_template = loader.get_template('dashboard/tables/actual_purchase/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
@group_required(['shop-owner'])
def actual_purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PurchaseForm()
    return render(request, 'actual_purchase_form.html', {'form': form})

@login_required()
@group_required(['shop-owner'])
def actual_purchase_edit(request, pk):
    actual_purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=actual_purchase)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PurchaseForm(instance=actual_purchase)
    return render(request, 'actual_purchase_form.html', {'form': form})