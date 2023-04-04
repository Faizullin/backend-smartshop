from rest_framework import serializers
from .models import Shop, Product,Purchase,PurchaseItem, CustomUser, ProductType


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id','name','created_at','updated_at']
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')

class ProductTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductType
        fields = ['id','name','image','created_at','updated_at']

    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        else:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri('/media/product_type/unknown-product_type.jpg')
            raise Exception("Incorrect concatenation for url with media: No request "+str(self.context))
        
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id','name', 'description','image', 'price','shop','type','created_at','updated_at']
    
    
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')
    
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        else:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri('/media/product/image/unknown-product.jpg')
            raise Exception("Incorrect concatenation for url with media: No request "+str(self.context))



class PurchaseItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    qty = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)
    shop = ShopSerializer(required= False)#serializers.IntegerField(required = False,)
    price = serializers.FloatField(required=False)
    class Meta:
        model = PurchaseItem
        fields = ['id','price','shop','quantity','qty']


class PurchaseSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,)

    class Meta:
        model = Purchase
        fields = ['id','user', 'products','total_price','status','created_at','updated_at']

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')


class PurchaseOrderSerializer(serializers.ModelSerializer):
    products = PurchaseItemSerializer(many=True,)

    class Meta:
        model = Purchase
        fields = ['id','user', 'products','total_price','status']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        product_ids = [product['id'] for product in products_data ]
        products = Product.objects.filter(id__in = product_ids)
        product_dict = {product.id: product for product in products}

        if len(products_data) > 0:
            total_price = 0
            purchase = Purchase.objects.create(user = validated_data['user'],total_price = 0, status="PENDING")

            for i in range(len(products_data)):
                product_id = products_data[i]['id']
                if product_id not in product_dict.keys():
                    raise serializers.ValidationError(f"Product with id={product_id} not found")  
            for i in range(len(products_data)):
                product_id = products_data[i]['id']
                qty = 1
                if 'qty' in products_data[i].keys():
                    qty = int(products_data[i]['qty'])
                shop = Shop.objects.get(id = product_dict[product_id].shop_id)
                purchase_item = PurchaseItem.objects.create(
                    product = product_dict[product_id],
                    purchase = purchase,
                    quantity = qty,
                    price = product_dict[product_id].price,
                    shop = shop,
                ) 
                total_price += (qty * purchase_item.price)
            purchase.total_price = total_price
            purchase.save()
            return purchase
        raise serializers.ValidationError(f"Empty products")  
        return None



class PurchaseOrderByBotSerializer(serializers.ModelSerializer):
    products = PurchaseItemSerializer(many=True,)

    class Meta:
        model = Purchase
        fields = ['id','user', 'products','total_price','status']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        product_ids = [product['id'] for product in products_data ]
        products = Product.objects.filter(id__in = product_ids)
        product_dict = {product.id: product for product in products}

        if len(products_data) > 0:
            total_price = 0
            purchase = Purchase.objects.create(user = validated_data['user'],total_price = 0, status="PENDING")

            for i in range(len(products_data)):
                product_id = products_data[i]['id']
                if product_id not in product_dict.keys():
                    raise serializers.ValidationError(f"Product with id={product_id} not found")  
            for i in range(len(products_data)):
                product_id = products_data[i]['id']
                qty = 1
                if 'qty' in products_data[i].keys():
                    qty = int(products_data[i]['qty'])
                shop = Shop.objects.get(id = product_dict[product_id].shop_id)
                purchase_item = PurchaseItem.objects.create(
                    product = product_dict[product_id],
                    purchase = purchase,
                    quantity = qty,
                    price = product_dict[product_id].price,
                    shop = shop,
                ) 
                total_price += (qty * purchase_item.price)
            purchase.total_price = total_price
            purchase.save()
            return purchase
        return None

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'address','username']