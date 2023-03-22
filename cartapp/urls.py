from django.urls import path

from cartapp.views import ViewCartAPIView, AddToCartAPIView, CartItemUpdateView, CartItemDeleteView, CheckoutView, \
    CancelOrderedItemView

urlpatterns = [
    path('view-cart/', ViewCartAPIView.as_view(), name='view-cart'),
    path('add_item-cart/', AddToCartAPIView.as_view(), name='add_item-cart'),
    path('update_item-cart/<int:cart_item_id>/', CartItemUpdateView.as_view(), name='update_item-cart'),
    path('delete_item-cart/<int:cart_item_id>/', CartItemDeleteView.as_view(), name='delete_item-cart'),
    path('checkout-cart/', CheckoutView.as_view(), name='checkout_items-cart'),
    path('cancel_ordered_item/<int:ordered_item_id>/', CancelOrderedItemView.as_view(), name='cancel_ordered_item'),
]



