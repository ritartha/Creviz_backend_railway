from django.conf import settings
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.discord import send_discord_notification

from .models import Commission
from .serializers import CommissionSerializer, CommissionStatusSerializer


class CommissionViewSet(viewsets.ModelViewSet):
    """
    POST   /api/commissions/                      submit request (public)
    GET    /api/commissions/                      list all (admin)
    GET    /api/commissions/{id}/                 retrieve one (admin)
    PATCH  /api/commissions/{id}/update_status/   update status (admin)
    """
    queryset         = Commission.objects.all()
    serializer_class = CommissionSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ["full_name", "email", "commission_type"]
    ordering         = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        commission = serializer.save()
        send_discord_notification(
            webhook_url = settings.DISCORD_WEBHOOK_COMMISSION,
            title       = "New Commission Request",
            color       = 0xFF2D2D,
            fields      = [
                {"name": "Name",
                 "value": commission.full_name,       "inline": True},
                {"name": "Email",
                 "value": commission.email,           "inline": True},
                {"name": "Type",
                 "value": commission.commission_type, "inline": True},
                {"name": "Budget",
                 "value": commission.budget,          "inline": True},
                {"name": "Deadline",
                 "value": str(commission.deadline or "Not specified"),
                 "inline": True},
                {"name": "Description",
                 "value": commission.description[:500], "inline": False},
            ],
        )

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[permissions.IsAdminUser],
    )
    def update_status(self, request, pk=None):
        """Update status and/or admin notes for a commission."""
        commission = self.get_object()
        serializer = CommissionStatusSerializer(
            commission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CommissionSerializer(commission).data)