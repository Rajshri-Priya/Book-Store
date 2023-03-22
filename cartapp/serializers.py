from rest_framework import serializers

from book.models import Book
from .models import Cart, CartItem, OrderedItem, Ordered


class CartItemSerializer2(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    quantity = serializers.IntegerField(default=0)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity']

    def create(self, validated_data):
        user = self.context.get('user')
        book = validated_data.get('book')
        quantity = validated_data.get('quantity')

        try:
            cart = Cart.objects.get(user=user, status='active')
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user, status='active')

        # check if cart item already exists for the given book
        cart_item = CartItem.objects.filter(cart=cart, book=book).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, book=book, quantity=quantity)

        cart.total_quantity += quantity
        cart.total_price += book.price * quantity
        cart.save()

        return cart_item

    def update(self, instance, validated_data):
        # Get the new quantity from the validated data
        quantity = validated_data.get('quantity')

        # Set the new quantity on the instance and save it
        if quantity == 0:
            instance.delete()
        else:
            instance.quantity = quantity
            instance.save()
        # Update cart total_quantity and total_price
        cart_items = CartItem.objects.filter(cart=instance.cart)
        instance.cart.total_quantity = sum([item.quantity for item in cart_items])
        instance.cart.total_price = sum([item.book.price * item.quantity for item in cart_items])
        instance.cart.save()

        # Return the updated instance
        return instance


class OrderedItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    status = serializers.CharField(required=True)

    class Meta:
        model = OrderedItem
        fields = ['id', 'book', 'quantity', 'price', 'total_price', 'status']

    def get_book(self, obj):
        return obj.book.title

    def get_price(self, obj):
        return obj.book.price

    def get_total_price(self, obj):
        return obj.quantity * obj.book.price

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('status') == OrderedItem.CANCELLED and instance.status == OrderedItem.CANCELLED:
            instance.book.quantity += instance.quantity
            instance.book.save()
        return instance


class CheckoutSerializer(serializers.Serializer):
    def create(self, validated_data):
        user = self.context['user']
        cart = self.context['cart']

        # create a new order
        ordered = Ordered.objects.create(user=user, total_quantity=cart.total_quantity, total_price=cart.total_price)

        # iterate over cart items and create ordered items
        for cart_item in cart.cartitem_set.all():
            # check if the book quantity is available in seller's stock
            if cart_item.book.quantity >= cart_item.quantity:
                # reduce the book quantity from seller's stock
                cart_item.book.quantity -= cart_item.quantity
                cart_item.book.save()

                # create ordered item
                OrderedItem.objects.create(ordered=ordered, book=cart_item.book, quantity=cart_item.quantity)
                cart_item.delete()
            else:
                raise serializers.ValidationError(f"Not enough stock available for book {cart_item.book.title}")

        # clear cart and update cart status
        cart.total_quantity = 0
        cart.total_price = 0
        cart.save()

        return ordered

    def validate(self, data):
        user = self.context['user']
        cart = self.context['cart']

        if cart.total_quantity == 0:
            raise serializers.ValidationError('Cannot checkout empty cart')

        return data


class CartSerializer(serializers.ModelSerializer):
    # items = CartItemSerializer2(many=True, read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'total_quantity', 'total_price', 'status', 'items']

    def get_items(self, obj):
        # Get all cart items in the cart
        cart_items = CartItem.objects.filter(cart=obj)

        # Create a dictionary to store each unique book item and its quantity
        unique_items = {}

        # Iterate over the cart items and update the quantity of the unique items(only for quantity get cart list)
        for item in cart_items:
            key = (item.book.id, item.book.title, item.book.author, item.book.price)
            if key in unique_items:
                unique_items[key]['quantity'] += item.quantity
            else:
                unique_items[key] = {'item_id': item.id,
                                     'book_id': item.book.id,
                                     'title': item.book.title,
                                     'author': item.book.author,
                                     'price': item.book.price,
                                     'quantity': item.quantity}

        # Return the list of unique book items
        return list(unique_items.values())
