from rest_framework import serializers

from products.utils import delete_image
from products.models import Product,Order,OrderItem,Category,Brand,Comment
from products.validators import (category_id_validator,brand_id_validator,product_id_validator,
                                 reply_to_id_validator)



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=['id','name','description']
        read_only_fields=['id']

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model=Brand
        fields=['id','name','description']
        read_only_fields=['id']


class ProductSerializer(serializers.ModelSerializer):

    category_id=serializers.IntegerField(write_only=True,validators=[category_id_validator])
    brand_id=serializers.IntegerField(write_only=True,validators=[brand_id_validator])
    class Meta:
        model=Product
        fields=[
            'id',
            'name',
            'description',
            'other_product_details',
            'price',
            'color',
            'image',
            'category',
            'category_id',
            'brand',
            'brand_id'
        ]
        read_only_fields=['category','brand','id','image']
        depth=1

    def create(self, validated_data):

        category_id=validated_data.pop('category_id')
        brand_id=validated_data.pop('brand_id')
        product=Product.objects.create(category_id=category_id,brand_id=brand_id,**validated_data)
        return product
    
    

class OrderItemCreateSerializer(serializers.Serializer):

    product=serializers.IntegerField()
    quantity=serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderItem
        fields=['product','quantity']
        depth = 1

    
class OrderSerializer(serializers.ModelSerializer):

    items=OrderItemCreateSerializer(many=True,write_only=True)
    order_items=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Order
        fields=['id','user','items','order_items','total_price']
        read_only_fields=['total_price','id','user']

    def get_order_items(self,obj):

        ord=obj.orderitem_set.all()
        ser=OrderItemSerializer(ord,many=True).data
        return ser
    def _create_order_items(self,items,order):

        total=0
        for item in items:
            print(item)
            item=dict(item)
            product=Product.objects.get(id=item['product'])
            total+=product.price*item['quantity']
            OrderItem.objects.create(product=product,order=order,quantity=item['quantity'])
        return total

    def create(self, validated_data):

        items=validated_data.pop('items')
        order=Order.objects.create(**validated_data)
        total=self._create_order_items(items,order)
        order.total_price=total
        order.save()
        return order

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=['id','image']
        read_only_fields=['id']
        extra_kwargs={'image':{'required':'True'}}

    def update(self, instance, validated_data):
        if instance.image:
            delete_image(instance.image)
        return super().update(instance, validated_data)
    

class CommentSerializer(serializers.ModelSerializer):
    
    product_id=serializers.IntegerField(write_only=True,validators=[product_id_validator])
    reply_to_id=serializers.IntegerField(write_only=True,required=False,validators=[reply_to_id_validator])
    replies=serializers.SerializerMethodField(read_only=True)
    name=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Comment
        fields=['id','user','name','content','product_id','reply_to_id','product','reply_to','replies']
        read_only_fields=['id','user','product','reply_to']

    def get_replies(self,obj):
        replies=Comment.objects.filter(reply_to=obj.id)
        ser=CommentSerializer(replies,many=True).data
        return ser

    def get_name(self,obj):
        return obj.user.name

    def create(self, validated_data):
        product_id=validated_data.pop('product_id')
        reply_to_id=validated_data.pop('reply_to_id',None)
        comment=Comment.objects.create(product_id=product_id,reply_to_id=reply_to_id,**validated_data)
        comment.save()
        return comment
    
class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Comment
        fields=['content']
        