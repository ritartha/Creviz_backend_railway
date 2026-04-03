from django.conf import settings
from rest_framework import filters, permissions, viewsets

from apps.core.discord import send_discord_notification

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    POST   /api/contact/          send a message (public)
    GET    /api/contact/          list all messages (admin)
    GET    /api/contact/{id}/     retrieve one (admin)
    """
    queryset         = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ["full_name", "email", "subject"]
    ordering         = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        msg = serializer.save()
        send_discord_notification(
            webhook_url = settings.DISCORD_WEBHOOK_CONTACT,
            title       = "New Contact Message",
            color       = 0x60A5FA,
            fields      = [
                {"name": "Name",
                 "value": msg.full_name, "inline": True},
                {"name": "Email",
                 "value": msg.email,     "inline": True},
                {"name": "Subject",
                 "value": msg.subject,   "inline": False},
                {"name": "Message",
                 "value": msg.message[:500], "inline": False},
            ],
        )