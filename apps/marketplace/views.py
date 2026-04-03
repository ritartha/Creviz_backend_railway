from django.conf import settings
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.discord import send_discord_notification

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD for marketplace products.

    GET    /api/marketplace/products/            list
    POST   /api/marketplace/products/            create  (admin)
    GET    /api/marketplace/products/{id}/       retrieve
    PUT    /api/marketplace/products/{id}/       update  (admin)
    PATCH  /api/marketplace/products/{id}/       partial (admin)
    DELETE /api/marketplace/products/{id}/       delete  (admin)
    GET    /api/marketplace/products/featured/   featured list

    Query params:
      ?category=character
      ?featured=true
      ?min_price=500
      ?max_price=2000
      ?search=warrior
    """
    queryset = Product.objects.filter(is_active=True).prefetch_related(
        "badges", "software", "formats"
    )
    serializer_class   = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ["title", "description", "category"]
    ordering_fields    = ["price", "rating", "downloads", "created_at"]
    ordering           = ["-featured", "-created_at"]

    def get_queryset(self):
        qs        = super().get_queryset()
        category  = self.request.query_params.get("category")
        featured  = self.request.query_params.get("featured")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        if category:
            qs = qs.filter(category=category)
        if featured == "true":
            qs = qs.filter(featured=True)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        return qs

    @action(detail=False, methods=["get"])
    def featured(self, request):
        """Return only featured products."""
        qs         = self.get_queryset().filter(featured=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Create and manage orders.

    POST   /api/marketplace/orders/                    place order (auth)
    GET    /api/marketplace/orders/                    list orders
    GET    /api/marketplace/orders/{id}/               retrieve one
    PATCH  /api/marketplace/orders/{id}/update_status/ update status (admin)
    """
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends    = [filters.OrderingFilter]
    ordering           = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().select_related("product", "user")
        return Order.objects.filter(user=user).select_related("product")

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        order   = serializer.save(
            user   = self.request.user,
            amount = product.price,
        )
        # Increment download counter
        Product.objects.filter(pk=product.pk).update(
            downloads=product.downloads + 1
        )
        # Notify Discord
        send_discord_notification(
            webhook_url = settings.DISCORD_WEBHOOK_ORDER,
            title       = "New Order Received",
            color       = 0xFF6B1A,
            fields      = [
                {"name": "Product",  "value": product.title,      "inline": True},
                {"name": "Amount",   "value": str(order.amount),  "inline": True},
                {"name": "Customer", "value": order.full_name,    "inline": True},
                {"name": "Email",    "value": order.email,        "inline": True},
            ],
        )

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[permissions.IsAdminUser],
    )
    def update_status(self, request, pk=None):
        """Admin-only: update the status of an order."""
        order      = self.get_object()
        new_status = request.data.get("status")
        valid      = [s[0] for s in Order.STATUS_CHOICES]
        if new_status not in valid:
            return Response(
                {"detail": "Status must be one of: {}".format(valid)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)