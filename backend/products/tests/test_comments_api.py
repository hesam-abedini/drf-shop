"""
test for comments api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal

from products.models import Product,Category,Brand,Comment
from products.serializers import CommentSerializer

COMMENT_URL=reverse('comment-create')

def comment_detail_url(comment_id,action):
    return reverse(f'comment-{action}',args=[comment_id])

def comment_list_url(product_id):
    return reverse(f'comment-list',kwargs={'pid':product_id})

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



class CommentTests(TestCase):
    def setUp(self):
        self.client=APIClient()
        self.category=Category.objects.create(name='test category',description='test')
        self.brand=Brand.objects.create(name='test brand',description='test')
        self.user=get_user_model().objects.create_user(
            email='test@example.com',
            password='ABcs23'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_comments(self):

        product=create_product(brand=self.brand,category=self.category)
        comment=Comment.objects.create(content='testst',product_id=product.id,user=self.user)
        comment2=Comment.objects.create(content='testst',product_id=product.id,user=self.user)
        url=comment_list_url(product.id)
        res=self.client.get(url,format='json')
        comments=Comment.objects.filter(product=int(product.id),reply_to__isnull=True).order_by('id')
        serilaizer=CommentSerializer(comments,many=True)
        self.assertEqual(res.data['results'],serilaizer.data)


    def test_create_comment(self):

        product=create_product(category=self.category,brand=self.brand)
        payload={
            'content':'testtest',
            'product_id':product.id
        }

        res=self.client.post(COMMENT_URL,format='json',data=payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

    def test_update_comment(self):

        product=create_product(category=self.category,brand=self.brand)
        comment=Comment.objects.create(content='testst',product_id=product.id,user=self.user)
        update={
            'content':'updated'
        }
        url=comment_detail_url(comment.id)

        res=self.client.patch(url,format='json',data=update)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['content'],update['content'])

    def test_update_comment(self):

        product=create_product(category=self.category,brand=self.brand)
        comment=Comment.objects.create(content='testst',product_id=product.id,user=self.user)
        update={
            'content':'updated'
        }
        url=comment_detail_url(comment.id,'update')

        res=self.client.patch(url,format='json',data=update)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data['content'],update['content'])

    def test_delete_comment(self):

        product=create_product(category=self.category,brand=self.brand)
        comment=Comment.objects.create(content='testst',product_id=product.id,user=self.user)

        url=comment_detail_url(comment.id,'delete')

        res=self.client.delete(url,format='json')
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
