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
def purchase_history_index(request):
    purchase_historys = Purchase.objects.all()#filter(status = "PENDING")
    context = {
        'segment': 'purchase_history_index',
        'purchase_historys': purchase_historys,
        'form': PurchaseForm()
    }
    html_template = loader.get_template('dashboard/tables/purchase_history/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required()
@group_required(['shop-owner'])
def purchase_history_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PurchaseForm()
    return render(request, 'purchase_history_form.html', {'form': form})

@login_required()
@group_required(['shop-owner'])
def purchase_history_edit(request, pk):
    purchase_history = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase_history)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PurchaseForm(instance=purchase_history)
    return render(request, 'purchase_history_form.html', {'form': form})











from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables
import django_filters
from django_filters.views import FilterView 



from shop_app.models import *
from .forms import *
from dashboard.decorators import group_required, OwnerRequiredMixin

@login_required()
@group_required(['shop-owner'])
def purchase_history_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = PurchaseForm(user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
@group_required(['shop-owner'])
def purchase_history_edit(request, pk):
    purchase_history = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES, instance=purchase_history)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        # else:
        #     return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PurchaseForm(instance=purchase_history, user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:purchase_history_edit', kwargs={'pk': purchase_history.pk}) })

@login_required
@group_required(['shop-owner'])
def purchase_history_delete(request, pk):
    purchase_history = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        purchase_history.delete()
        return redirect('dashboard:purchase_history_index')
    raise Http404

class PurchaseFilter(django_filters.FilterSet):
    class Meta:
        model = Purchase
        fields = ['id', 'user',]

class PurchaseTable(tables.Table):
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:purchase_history_edit\' pk=record.pk %}">Edit</a>'
                '<a class="">'
                    '<form method="post" action="{% url \'dashboard:purchase_history_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = Purchase
        fields = ("id","user", "total_price",  "created_at" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }
    
    def render_user(self, value, record):
        return f"{value.username}({value.pk})"

class PurchaseListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = Purchase
    table_class = PurchaseTable
    template_name = 'dashboard/tables/purchase_history/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = PurchaseFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = PurchaseForm()
        return context
    
    def get_queryset(self, *args, **kwargs):
        shops = Shop.objects.filter(owner = self.request.user)
        shop_ids = [shop.id for shop in shops]
        purchase_items = PurchaseItem.objects.filter(shop_id__in = shop_ids)
        purchase_item_ids = set([purchase_item.purchase_id for purchase_item in purchase_items])
        return Purchase.objects.filter(id__in = purchase_item_ids, status = "DELIVERED")