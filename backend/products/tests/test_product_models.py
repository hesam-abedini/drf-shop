"""
test for product models
"""
from decimal import Decimal

from django.test import TestCase
from products.models import Product,Category,Brand,Comment,Order,OrderItem
from django.contrib.auth import get_user_model

class ProductModelsTests(TestCase):
    """
    test product models
    """
    category={
        "name":'test category',
        "description":'testing'
    }
    brand={
        "name":'test brand',
        "description":'testing'
    }
    product={
        'name':'test product',
        'description':'test desc',
        'price':Decimal('96.50'),
        'color':'black'
    }
    def test_create_category(self):

        category=Category.objects.create(**self.category)
        self.assertEqual(category.name,self.category['name'])
        self.assertEqual(category.description,self.category['description'])

    def test_create_brand(self):

        brand=Brand.objects.create(**self.brand)
        self.assertEqual(brand.name,self.brand['name'])
        self.assertEqual(brand.description,self.brand['description'])   

    def test_create_product(self):
        category=Category.objects.create(**self.category)
        brand=Brand.objects.create(**self.brand)
        product=Product.objects.create(category=category,brand=brand,**self.product)
        self.assertEqual(product.name,self.product['name'])
        self.assertEqual(product.description,self.product['description'])
        self.assertEqual(product.category.name,self.category['name'])
        self.assertEqual(product.brand.name,self.brand['name'])

    def test_comment(self):
        user=get_user_model().objects.create_user(email='test@example.com',password='Abvs24')
        category=Category.objects.create(**self.category)
        brand=Brand.objects.create(**self.brand)
        product=Product.objects.create(category=category,brand=brand,**self.product)
        content='test1234'
        comment=Comment.objects.create(user=user,product=product,content=content)
        self.assertEqual(comment.content,content)
        self.assertEqual(comment.user.id,user.id)
        self.assertEqual(comment.product.id,product.id)

    def test_order_and_orderitem(self):
        category=Category.objects.create(**self.category)
        brand=Brand.objects.create(**self.brand)
        product=Product.objects.create(category=category,brand=brand,**self.product)
        user=get_user_model().objects.create_user(email='test@example.com',password='Abvs24')
        total_price=Decimal('250.50')
        quantity=2

        order=Order.objects.create(user=user,total_price=total_price)
        order_item=OrderItem.objects.create(product=product,order=order,quantity=quantity)
        self.assertEqual(order.user.id,user.id)
        self.assertEqual(order_item.order.id,order.id)
        self.assertEqual(order_item.product.id,product.id)
        self.assertEqual(order_item.quantity,quantity)

    