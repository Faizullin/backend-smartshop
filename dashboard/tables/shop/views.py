from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from dashboard.decorators import group_required
from shop_app.models import *
from .forms import *

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
def shop_create(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            form.save()
            return JsonResponse({'success': True})
    else:
        form = ShopForm(user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
@group_required(['shop-owner'])
def shop_edit(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = ShopForm(instance=shop)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:shop_edit', kwargs={'pk': shop.pk}) })

@login_required
@group_required(['shop-owner'])
def shop_delete(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        shop.delete()
        return redirect('dashboard:shop_index')
    raise Http404

class ShopFilter(django_filters.FilterSet):
    class Meta:
        model = Shop
        fields = ['id', 'name']
    
class ShopTable(tables.Table):
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:shop_edit\' pk=record.pk %}">Edit</a>'
                '<a class="dropdown-item" href="{% url \'dashboard:product_index\' %}?shop={{ record.pk }}">Products</a>'
                '<a class="">'
                    '<form method="post" action="{% url \'dashboard:shop_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = Shop
        fields = ("id","name","address", "created_at" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }

class ShopListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = Shop
    table_class = ShopTable
    template_name = 'dashboard/tables/shop/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = ShopFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = ShopForm()
        context['segment'] = 'shop_index'
        return context
    
    def get_queryset(self, *args, **kwargs):
        return Shop.objects.filter(owner = self.request.user)