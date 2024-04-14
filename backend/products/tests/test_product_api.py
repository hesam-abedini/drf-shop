"""
test for product api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal

from products.models import Product,Category,Brand
from products.serializers import ProductSerializer,CategorySerializer,BrandSerializer

PRODUCT_URL=reverse('product-list-create')
CATEGORY_URL=reverse('category-list')
BRAND_URL=reverse('brand-list')

def product_url(product_id,action):
    return reverse(f'product-{action}',args=[product_id])

def category_detail_url(category_id):
    return reverse('category-detail',args=[category_id])

def brand_detail_url(brand_id):
    return reverse('brand-detail',args=[brand_id])



def create_product(**params):

    defaults={
        'name':'product 1',
        'description':'test',
        'price':Decimal('25.50'),
        'color':'red'
    }
    defaults.update(params)
    product=Product.objects.create(**defaults)
    return product


class PublicProductTests(TestCase):

    def setUp(self):
        self.client=APIClient()
        self.category=Category.objects.create(name='test category',description='test')
        self.brand=Brand.objects.create(name='test brand',description='test')

    def test_retrive_products(self):

        create_product(category_id=self.category.id,brand_id=self.brand.id)
        create_product(category_id=self.category.id,brand_id=self.brand.id)

        res=self.client.get(PRODUCT_URL)
        products=Product.objects.all().order_by('-id')
        serializer=ProductSerializer(products,many=True)
        self.assertEqual(res.data['results'],serializer.data)

    def test_retrive_category(self):

        res=self.client.get(CATEGORY_URL)
        categories=Category.objects.all().order_by('-id')
        serializer=CategorySerializer(categories,many=True)
        self.assertEqual(res.data,serializer.data)

    def test_retrive_brand(self):

        res=self.client.get(BRAND_URL)
        brands=Brand.objects.all().order_by('-id')
        serializer=BrandSerializer(brands,many=True)
        self.assertEqual(res.data,serializer.data)


class PrivateProductTests(TestCase):

    def setUp(self):
        self.client=APIClient()
        self.user=get_user_model().objects.create_superuser(
            email='test@example.com',
            password='ABcs23'
        )
        self.client.force_authenticate(self.user)

    def test_create_product(self):

        category=Category.objects.create(name='test category',description='test')
        brand=Brand.objects.create(name='test brand',description='test')
        payload={
            'name':'product 1',
            'description':'test',
            'price':Decimal('25.50'),
            'color':'red',
            'category_id':category.id,
            'brand_id':brand.id
        }

        res=self.client.post(PRODUCT_URL,format='json',data=payload)       
        self.assertEqual(res.status_code,status.HTTP_201_CREATED) 
        self.assertEqual(res.data['name'],payload['name'])

    def test_update_product(self):

        category=Category.objects.create(name='test category',description='test')
        brand=Brand.objects.create(name='test brand',description='test')
        data={
            'name':'product 1',
            'description':'test',
            'price':Decimal('25.50'),
            'color':'red'
        }
        product=Product.objects.create(**data,category=category,brand=brand)
        update={
            'description':'test2',
            'color':'black'
        }
        url=product_url(product.id,'update')

        res=self.client.patch(url,format='json',data=update)
        self.assertEqual(res.data['description'],update['description'])
        self.assertEqual(res.data['color'],update['color'])

    def test_product_delete(self):

        category=Category.objects.create(name='test category',description='test')
        brand=Brand.objects.create(name='test brand',description='test')
        data={
            'name':'product 1',
            'description':'test',
            'price':Decimal('25.50'),
            'color':'red'
        }
        product=Product.objects.create(**data,category=category,brand=brand)
        url=product_url(product.id,'delete')

        res=self.client.delete(url,format='json')
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)


    def test_create_category(self):

        payload={
            'name':'category 1',
            'description':'test',
        }
        res=self.client.post(CATEGORY_URL,format='json',data=payload)       
        self.assertEqual(res.status_code,status.HTTP_201_CREATED) 
        self.assertEqual(res.data['name'],payload['name'])

    def test_update_category(self):

        category=Category.objects.create(name='test category',description='test')
        update={
            'name':'test category2'
        }
        url=category_detail_url(category.id)

        res=self.client.patch(url,format='json',data=update)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['name'],update['name'])

    def test_delete_category(self):

        category=Category.objects.create(name='test category',description='test')
        url=category_detail_url(category.id)

        res=self.client.delete(url,format='json')
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)

    def test_create_Brand(self):

        payload={
            'name':'brand 1',
            'description':'test',
        }
        res=self.client.post(BRAND_URL,format='json',data=payload)       
        self.assertEqual(res.status_code,status.HTTP_201_CREATED) 
        self.assertEqual(res.data['name'],payload['name'])

    def test_update_brand(self):

        brand=Brand.objects.create(name='test brand',description='test')
        update={
            'name':'test brand2'
        }
        url=brand_detail_url(brand.id)

        res=self.client.patch(url,format='json',data=update)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['name'],update['name'])

    def test_delete_brand(self):

        brand=Brand.objects.create(name='test brand',description='test')
        url=brand_detail_url(brand.id)

        res=self.client.delete(url,format='json')
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)