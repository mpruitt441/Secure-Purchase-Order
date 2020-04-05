from django.urls import path, include
from django.urls import path
from .views import (
    orderListView,
    orderDetailView,
    orderCreateView,
    orderUpdateView,
    orderDeleteView,
    orderApproveView,
    orderPurchaseView
)
from . import views

urlpatterns = [
    path('', orderListView.as_view(), name='purchaseorder-home'),
    path('order/<int:pk>/', orderDetailView.as_view(), name='order-detail'),
    path('order/new/', orderCreateView.as_view(), name='order-create'),
    path('order/<int:pk>/update/', orderUpdateView.as_view(), name='order-update'),
    path('order/<int:pk>/approve/', orderApproveView.as_view(), name='order-approve'),
    path('order/<int:pk>/purchase/', orderPurchaseView.as_view(), name='order-purchase'),
    path('order/<int:pk>/delete/', orderDeleteView.as_view(), name='order-delete'),
    path('about/',views.about,name='purchaseorder-about'),
]
