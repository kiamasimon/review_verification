from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from commerce import views
from commerce.views import OrderViewSet, OrderItemViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.ProductCategoryViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'address', views.AddressViewSet)
router.register(r'orders', views.OrderViewSet, basename='orders')
# router.register(r'order_items', views.OrderItemViewSet, basename='order_items')
# order_items = OrderItemViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # path('/order/items/<int:order_id>', order_items, name='order_items'),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),

    path('product/reviews/<int:product_id>/', views.product_comments),

    path('login', views.get_access_token),
    path('cart', views.get_cart),
]