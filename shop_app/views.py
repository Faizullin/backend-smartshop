from django.shortcuts import render
from django.middleware.csrf import get_token
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Shop, Product, Purchase, ProductType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions,generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import  JWTAuthentication


def index(request):
    return render(request, 'app.html', {
        'MyDebug': settings.MY_DEBUG,
    })



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
            data['canOpenDashboard'] = user_data.groups.filter(name="shop-owner").exists()
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

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class IdListFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        id_list = request.query_params.getlist('ids')
        id_list = [int(id) for id in id_list]
        if id_list:
            queryset = queryset.filter(id__in=id_list)
        return queryset
    
class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [IdListFilterBackend,DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['type','shop']
    search_fields = ['name']
    ordering_fields = ['created_at','name']

class ProductFiltersView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        shops = Shop.objects.all()
        shops_data = ShopSerializer(shops, many=True).data
        product_types = ProductType.objects.all()
        product_types_data = ProductTypeSerializer(product_types, many=True, context = {'request':request}).data

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
        data = {
            'user': request.user.id, 
            'status': "PENDING", 
            'products': request.data.get('products'),
            'total_price': 0,
        }
        serializer = PurchaseOrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsBot(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['bot']).exists()

class PurchaseOrderByBotView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = (permissions.IsAuthenticated, IsBot)
    serializer_class = PurchaseOrderByBotSerializer
    def post(self, request, *args, **kwargs):        
        data = {
            'user': request.data.get('user'),
            'status': "PENDING", 
            'products': request.data.get('products'),
            'total_price': 0,
        }
        serializer = PurchaseOrderByBotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CsrfTokenView(APIView):
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token})