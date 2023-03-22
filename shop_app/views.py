from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import Shop, Product, Purchase, ProductType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, permissions,generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import  JWTAuthentication


# def main_app(request):
#     return render(request,"app.html",{
#         'fornt_url': 'http://localhost:3000',
#     })
    
def index(request):
    if request.method == 'POST':
        return HttpResponse(str("Hi"))
    return render(request, 'app.html', {'statistics': {
     'temperature': 0,
    }})



class AuthProfileView(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            user_data = CustomUser.objects.filter(id=user.id).first()
            data = UserProfileSerializer(user_data).data
            data['name'] = data['username']
            data['age'] = 18
            data['canDashboard'] = user_data.groups.filter(name="shop-owner").exists()
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': f"No user data with id {user} found"}, status=status.HTTP_404_NOT_FOUND)

class AuthOrdersView(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            user_data = Purchase.objects.get(user = user)
            return Response(PurchaseSerializer(user_data).data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)

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
    authentication_classes = [JWTAuthentication, ]
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        qs = super().get_queryset() 
        user = self.request.user
        return qs.filter(user = user)

        
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

