from django.urls import path,include
from rest_framework.routers import DefaultRouter


from products.views import (ProductDetailAPIView,
                            ProdcutListCreateAPIView,
                            ProductUpdateAPIView,
                            ProductDestroyAPIView,
                            OrderListCreateAPIView,
                            OrderDetailAPIView,
                            CategoryViewSet,
                            BrandViewSet,
                            ProductImageUpdateAPIView,
                            CommentCreateAPIView,
                            CommentListAPIView,
                            CommentUpdateAPIView,
                            CommentDeleteAPIView)

router=DefaultRouter()
router.register('category',CategoryViewSet)
router.register('brand',BrandViewSet)

urlpatterns=[
    path('',ProdcutListCreateAPIView.as_view(),name='product-list-create'),
    path('',include(router.urls)),
    path('<int:pk>/update/',ProductUpdateAPIView.as_view(),name='product-update'),
    path('<int:pk>/update-image/',ProductImageUpdateAPIView.as_view()),
    path('<int:pk>/delete/',ProductDestroyAPIView.as_view(),name='product-delete'),
    path('<int:pk>/',ProductDetailAPIView.as_view(),name='product-detail'),
    path('<int:pid>/comment/',CommentListAPIView.as_view(),name='comment-list'),
    path('order/',OrderListCreateAPIView.as_view(),name='order-list-create'),
    path('comment/',CommentCreateAPIView.as_view(),name='comment-create'),
    path('comment/<int:pk>/update/',CommentUpdateAPIView.as_view(),name='comment-update'),
    path('comment/<int:pk>/delete/',CommentDeleteAPIView.as_view(),name='comment-delete'),
    path('order/<int:pk>/',OrderDetailAPIView.as_view(),name='order-detail'),
]