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
        purchase_form = PurchaseForm(request.POST)
        purchase_item_formset = purchase_form.purchase_items(request.POST)

        if purchase_form.is_valid() and purchase_item_formset.is_valid():
            purchase = purchase_form.save(commit=False)
            purchase.save()

            for form in purchase_item_formset:
                purchase_item = form.save(commit=False)
                purchase_item.purchase = purchase
                purchase_item.save()
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        purchase_form = PurchaseForm(user=request.user)
        purchase_item_formset = purchase_form.purchase_items()

    return render(request, 'dashboard/tables/purchase/form_base.html', {
        'purchase_form': purchase_form,
        'purchase_item_formset': purchase_item_formset,
    })

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
        fields = ['id', 'user',"shop", "status",]

    
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
        fields = ("id","user","shop","status", "purchase_historys", "total_price", "created_at" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }
    
    # def render_shop(self, value, record):
    #     return f"{value.name}({value.pk})"
    # def render_type(self, value, record):
    #     return f"{value.name}({value.pk})"

class PurchaseHistoryListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = Purchase
    table_class = PurchaseTable
    template_name = 'dashboard/tables/purchase_history/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = PurchaseFilter
    table_data = Purchase.objects.filter(status =  [t[1] for t in Purchase.STATUS_CHOICES if t[0] == 'DELIVERED' ][0])
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = PurchaseForm()
        return context