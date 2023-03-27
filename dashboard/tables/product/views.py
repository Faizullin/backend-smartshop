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
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = ProductForm(user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
@group_required(['shop-owner'])
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        # else:
        #     return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm(instance=product, user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:product_edit', kwargs={'pk': product.pk}) })

@login_required
@group_required(['shop-owner'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:product_index')
    raise Http404

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['id', 'name',"shop", "type",]

class ImageColumn(tables.Column):
    def render(self, value):
        # if not value or not value.url:
        #     return '<img src="/media/product/image/unknown-product.jpg" />'
        return format_html('<img src="{}" width=\'50\' height=\'50\'/>', value.url)
    
class ProductTable(tables.Table):
    image = ImageColumn(orderable=False, default=format_html("<img src='/media/product/image/unknown-product.jpg' width=\'50\' height=\'50\'/>"))
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:product_edit\' pk=record.pk %}">Edit</a>'
                '<a class="dropdown-item" href="{% url \'dashboard:product_index\' %}?shop={{ record.shop.pk }}">Filter By Shop</a>'
                '<a class="">'
                    '<form method="post" action="{% url \'dashboard:product_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = Product
        #template_name = "django_tables2/bootstrap.html"
        fields = ("id","name","shop", "type", "image", "created_at" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }
    
    def render_shop(self, value, record):
        return f"{value.name}({value.pk})"
    def render_type(self, value, record):
        return f"{value.name}({value.pk})"

class ProductListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = Product
    table_class = ProductTable
    template_name = 'dashboard/tables/product/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = ProductFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = ProductForm(user= self.request.user)
        context['segment'] = 'product_index'
        return context
    def get_queryset(self, *args, **kwargs):
        shops = Shop.objects.filter(owner = self.request.user)
        shop_ids = [shop.id for shop in shops]
        return Product.objects.filter(shop_id__in = shop_ids)