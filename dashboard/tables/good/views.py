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
def product_index(request):
    products = Product.objects.all()
    context = {
        'segment': 'product_index',
        'products': products,
        'form': ProductForm()
    }
    html_template = loader.get_template('dashboard/tables/product/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
@group_required(['shop-owner'])
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required()
@group_required(['shop-owner'])
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})