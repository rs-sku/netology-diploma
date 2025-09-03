from django.core.mail import send_mail
from rest_framework import serializers

from online_shop.settings import EMAIL_HOST_USER
from orders.models import Contact, Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "dt": {"read_only": True},
        }

    def update(self, instance: Order, validated_data: dict) -> Order:
        if validated_data.get("status") == "confirmed" and validated_data.get("address") is not None:
            send_mail(
                "Подтверждение заказа",
                f"Заказ #{instance.id} подтвержден",
                EMAIL_HOST_USER,
                [instance.user.email],
            )
        return super().update(instance, validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
        }


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
        }
