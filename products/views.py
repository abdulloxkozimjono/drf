from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Product
from .serializers import OrderSerializer
from django.shortcuts import render

def home(request):
    products = Product.objects.filter(quantity__gt=0)
    orders = Order.objects.all().order_by('-created_at')

    # Statistikalarni hisoblash
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    stats = {
        'daily': sum(o.total_price for o in orders if o.created_at >= now - timedelta(days=1)),
        'weekly': sum(o.total_price for o in orders if o.created_at >= now - timedelta(weeks=1)),
        'monthly': sum(o.total_price for o in orders if o.created_at >= now - timedelta(days=30)),
        'yearly': sum(o.total_price for o in orders if o.created_at >= now - timedelta(days=365)),
    }

    return render(request, 'products/home.html', {'products': products, 'orders': orders, 'stats': stats})



@api_view(["POST"])
def create_order(request):
    """
    Botdan keladigan buyurtmalarni qabul qiladi
    """
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        product = Product.objects.get(id=request.data["product"])
        qty = int(request.data["quantity"])

        if product.quantity < qty:
            return Response({"error": "Omborda yetarli mahsulot yo‘q"}, status=400)

        # Buyurtmani saqlash
        order = serializer.save()

        # Ombordagi sonini kamaytirish
        product.quantity -= qty
        product.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(quantity__gt=0)  # faqat borlarini chiqaradi
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer

