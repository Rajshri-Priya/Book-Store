from rest_framework.views import APIView
from rest_framework.response import Response

from logging_config.logger import get_logger
from .models import Cart, CartItem, OrderedItem
from .serializers import CartSerializer, CartItemSerializer2, CheckoutSerializer, OrderedItemSerializer

# logging config
logger = get_logger()


class ViewCartAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            cart = Cart.objects.get(user=user, status='active')
            serializer = CartSerializer(cart)
            return Response({"success": True, "message": "Retrieve Cart List Successfully", "data": serializer.data,
                             "status": 200}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)


class AddToCartAPIView(APIView):

    def post(self, request):
        try:
            serializer = CartItemSerializer2(data=request.data, context={"user": request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True, "message": "Item added  Successfully", "data": serializer.data,
                             "status": 200}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)


class CartItemUpdateView(APIView):
    def put(self, request, cart_item_id):
        try:
            cart = Cart.objects.get(user=request.user.id, status='active')
            cart_item = CartItem.objects.get(id=cart_item_id, cart_id=cart)
            serializer = CartItemSerializer2(cart_item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "Message": "Book quantity updated successfully",
                 "data": serializer.data, "status": 200}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)


class CartItemDeleteView(APIView):
    def delete(self, request, cart_item_id):
        try:
            cart = Cart.objects.get(user=request.user.id, status='active')
            cart_item = CartItem.objects.get(id=cart_item_id, cart_id=cart)
            quantity = cart_item.quantity
            cart.total_quantity -= quantity
            cart.total_price -= cart_item.book.price * quantity
            cart.save()
            cart_item.delete()
            return Response({"success": True, "Message": "Book Item deleted successfully", 'status': 200})
        except Exception as e:
            logger.error(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)


class CheckoutView(APIView):
    def post(self, request):
        try:
            user = request.user
            try:
                cart = Cart.objects.get(user=user, status='active')
            except Cart.DoesNotExist:
                return Response({'message': 'No active cart found for this user'}, status=400)

            serializer = CheckoutSerializer(data={}, context={'user': user, 'cart': cart})
            print(serializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': True, 'message': 'Order placed successfully'}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

    def get(self, request):
        try:
            user = request.user
            order_items = OrderedItem.objects.filter(ordered__user=user)
            serializer = OrderedItemSerializer(order_items, many=True)
            return Response({"success": True, "message": "Retrieve ordered List Successfully", "data": serializer.data,
                             "status": 200}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)


class CancelOrderedItemView(APIView):
    def put(self, request, ordered_item_id):
        try:
            user = request.user
            try:
                ordered_item = OrderedItem.objects.get(id=ordered_item_id, ordered__user=user)
            except OrderedItem.DoesNotExist:
                return Response({'error': 'Ordered item not found or cannot be cancelled'},
                                status=404)

            # Update the status of the ordered item to cancelled
            ordered_item.status = 'cancelled'
            ordered_item.save()

            # Return the updated ordered item
            serializer = OrderedItemSerializer(instance=ordered_item, data={'status': 'cancelled'}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True, "message": "Order Cancelled Successfully", "data": serializer.data,
                             "status": 200}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)

