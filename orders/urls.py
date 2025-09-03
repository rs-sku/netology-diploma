from rest_framework.routers import DefaultRouter

from orders.views import ContactViewSet, OrderItemViewSet, OrderViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")
router.register("order-items", OrderItemViewSet, basename="order_items")
router.register("contacts", ContactViewSet, basename="contacts")

urlpatterns = router.urls