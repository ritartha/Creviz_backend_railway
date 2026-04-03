from rest_framework import serializers

from .models import Commission


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Commission
        fields = [
            "id", "full_name", "email", "commission_type",
            "budget", "deadline", "description", "reference_image",
            "status", "admin_notes", "created_at",
        ]
        read_only_fields = ["id", "status", "admin_notes", "created_at"]


class CommissionStatusSerializer(serializers.ModelSerializer):
    """Used by admin to update the status and internal notes only."""
    class Meta:
        model  = Commission
        fields = ["status", "admin_notes"]