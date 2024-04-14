from rest_framework import generics,viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters

from products.utils import delete_image
from app.pagination import StandardResultsSetPagination 
from products.permissions import CreatePermission,CommentDeletePermission,CommentEditPermission
from products.models import Product,Order,Category,Brand,Comment
from products.serializers import (ProductSerializer,OrderSerializer,CategorySerializer,
                                  ProductImageSerializer,BrandSerializer,CommentSerializer,
                                  CommentUpdateSerializer)



class CategoryViewSet(viewsets.ModelViewSet):

    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly,CreatePermission]

class BrandViewSet(viewsets.ModelViewSet):

    queryset=Brand.objects.all()
    serializer_class=BrandSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly,CreatePermission]


class ProdcutListCreateAPIView(generics.ListCreateAPIView):

    search_fields = ['name']
    ordering_fields = ['price']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly,CreatePermission]
    pagination_class=StandardResultsSetPagination

    def _params_to_ints(self,qs):
        return [int(str_id) for str_id in qs.split(',')]
    
    def get_queryset(self):

        queryset=self.queryset
        category=self.request.query_params.get('category')
        brand=self.request.query_params.get('brand')
        if category:
            queryset=queryset.filter(category__id=int(category))
        if brand:
            brand_ids=self._params_to_ints(brand)
            queryset=queryset.filter(brand__id__in=brand_ids)
        return queryset.all().order_by('-id')


class ProductDetailAPIView(generics.RetrieveAPIView):

    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):

    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]

class ProductDestroyAPIView(generics.DestroyAPIView):

    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]
    lookup_field='pk'

    def perform_destroy(self, instance):
        delete_image(instance.image)
        super().perform_destroy(instance)

class ProductImageUpdateAPIView(generics.UpdateAPIView):

    queryset=Product.objects.all()
    serializer_class=ProductImageSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]



class OrderListCreateAPIView(generics.ListCreateAPIView):

    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_class=StandardResultsSetPagination

    def get_queryset(self):

        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.queryset.all().order_by('-id')
        else:
            return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailAPIView(generics.RetrieveAPIView):

    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=self.request.user).order_by('-id')


class CommentCreateAPIView(generics.CreateAPIView):

    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentListAPIView(generics.ListAPIView):

    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    pagination_class=StandardResultsSetPagination

    def get_queryset(self):

        product_id=self.kwargs['pid']
        return self.queryset.filter(product=int(product_id),reply_to__isnull=True).order_by('id')
    

class CommentUpdateAPIView(generics.UpdateAPIView):

    serializer_class=CommentUpdateSerializer
    queryset=Comment.objects.all()
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,CommentEditPermission]
    
class CommentDeleteAPIView(generics.DestroyAPIView):
    
    serializer_class=CommentUpdateSerializer
    queryset=Comment.objects.all()
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,CommentDeletePermission]















