from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from orders.models import Contact, Order, OrderItem
from orders.serializers import (ContactSerializer, OrderItemSerializer,
                                OrderSerializer)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self) -> list:
        return [IsAuthenticated()]
    
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_permissions(self)-> list:
        return [IsAuthenticated()]
    
class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_permissions(self)-> list:
        return [IsAuthenticated()]
    
