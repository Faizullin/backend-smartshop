from django.shortcuts import render, HttpResponse
from .models import Shop, Product, Purchase, ProductType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, permissions,generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend

# def main_app(request):
#     return render(request,"app.html",{
#         'fornt_url': 'http://localhost:3000',
#     })
    
def index(request):
    if request.method == 'POST':
        return HttpResponse(str("Hi"))
        #activity_type = request.POST['activity_type']
        #user = request.user
        #log_activity.delay(activity_type, user)
    # statistics = get_activity_statistics.delay().get()
    #temperature = get_system_temperature.delay()
    return render(request, 'app.html', {'statistics': {
     'temperature': 0,
    }})


# class PurchaseView(APIView):
#     def get(self, request, *args, **kwargs):
#         purchase_id = kwargs.get('id')
#         if purchase_id:
#             try:
#                 purchase = Purchase.objects.get(id=purchase_id)
#                 return Response(GetPurchaseSerializer(purchase).data, status=status.HTTP_200_OK)
#             except ObjectDoesNotExist:
#                 return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             purchases = Purchase.objects.all()
#             purchases_data = PurchaseSerializer(purchases, many=True).data
#             return Response(data=purchases_data)

# class ProductView(APIView):
#     #authentication_classes = (TokenAuthentication,)
#     #permission_classes = (IsAuthenticated,)
#     def get(self, request, *args, **kwargs):
#         product_id = kwargs.get('id')
#         if product_id:
#             try:
#                 product = Product.objects.get(id=product_id)
#                 return Response(GetProductSerializer(product).data, status=status.HTTP_200_OK)
#             except ObjectDoesNotExist:
#                 return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             posts = Product.objects.all()
#             shop_filters = request.query_params.getlist('shops[]', None)
#             if shop_filters:
#                 posts = posts.filter(shop__id__in=shop_filters)
#             posts_data = ProductSerializer(posts, many=True,context={'request': request}).data
#             return Response(data=posts_data)

class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['type','shop']
    search_fields = ['name']
    ordering_fields = ['created_at','name']

    def get_object(self, product_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Product.objects.get(id=product_id, user = user_id)
        except Product.DoesNotExist:
            return None


class ProductFiltersView(APIView):
    def get(self, request, *args, **kwargs):
        shops = Shop.objects.all()
        shops_data = ShopSerializer(shops, many=True).data
        product_types = ProductType.objects.all()
        product_types_data = ProductTypeSerializer(product_types, many=True).data

        return Response(data={
            'product_types': product_types_data,
            'shops': shops_data,
        })
    
class PurchaseView(generics.ListAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    # def get(self, request, *args, **kwargs):
    #     purchase_id = kwargs.get('id')
    #     if purchase_id:
    #         try:
    #             purchase = Purchase.objects.get(id=purchase_id)
    #             return Response(GetPurchaseSerializer(purchase).data, status=status.HTTP_200_OK)
    #         except ObjectDoesNotExist:
    #             return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         purchases = Purchase.objects.all()
    #         purchases_data = PurchaseSerializer(purchases, many=True).data
    #         return Response(data=purchases_data)
        
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        #product = Purchase.object.filter(id__in=user_data)
        
        data = {
            'user': request.data.get('user'), 
            'status': request.data.get('status'), 
            'products': [],
            'total_price': request.data.get('total_price'),
            'shop': request.data.get('shop'),
            'product_items': request.data.get('product_items'),
        }

        serializer = PurchaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PurchaseOrderView(APIView):

    def post(self, request, format='jpg'):

    
        return Response(up_file.name, status.HTTP_201_CREATED)

class PurchaseOrderByBotView(APIView):
    def get(self, request, *args, **kwargs):
        purchase_id = kwargs.get('id')
        if purchase_id:
            try:
                purchase = Purchase.objects.get(id=purchase_id)
                return Response(GetPurchaseSerializer(purchase).data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            purchases = Purchase.objects.all()
            purchases_data = PurchaseSerializer(purchases, many=True).data
            return Response(data=purchases_data)

