from rest_framework import serializers
from .models import Shop, Product,Purchase


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
        model = Product
        fields = ['id','name','created_at','updated_at']
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')

class ProductSerializer(serializers.ModelSerializer):
    
    #created_at.strftime('%b %e %Y')
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
            return obj.image
        else:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri('/media/product/image/unknown-product.jpg')
            raise Exception("Incorrect concatenation for url with media: No request "+str(self.context))


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id','user', 'shop', 'products','total_price','status','created_at','updated_at']
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')
    
class GetPurchaseSerializer(serializers.ModelSerializer):
    #post_comments = CommentSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','user', 'shop', 'products','total_price','status','created_at','updated_at']
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')

class GetProductSerializer(serializers.ModelSerializer):
    #post_comments = CommentSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','name', 'description', 'price','shop','type','created_at','updated_at']
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B %Y')
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d %B %Y')