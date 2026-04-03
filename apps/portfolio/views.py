from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Anyone can read (GET, HEAD, OPTIONS).
    Only staff/admin can create, update or delete.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD for portfolio projects.

    GET    /api/portfolio/projects/            list
    POST   /api/portfolio/projects/            create  (admin)
    GET    /api/portfolio/projects/{id}/       retrieve
    PUT    /api/portfolio/projects/{id}/       update  (admin)
    PATCH  /api/portfolio/projects/{id}/       partial (admin)
    DELETE /api/portfolio/projects/{id}/       delete  (admin)
    POST   /api/portfolio/projects/reorder/    reorder (admin)

    Query params:
      ?category=environment
      ?search=ember
      ?visible=true   (default)
    """
    queryset           = Project.objects.all().prefetch_related("tools")
    serializer_class   = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ["title", "description", "category"]
    ordering_fields    = ["order", "created_at", "title"]
    ordering           = ["order"]

    def get_queryset(self):
        qs       = super().get_queryset()
        category = self.request.query_params.get("category")
        visible  = self.request.query_params.get("visible", "true")
        if category:
            qs = qs.filter(category=category)
        if visible.lower() == "true":
            qs = qs.filter(is_visible=True)
        return qs

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser],
    )
    def reorder(self, request):
        """
        Reorder projects by passing a list of IDs in the desired order.
        Body: { "order": [3, 1, 5, 2, 4] }
        """
        ids = request.data.get("order", [])
        if not ids:
            return Response(
                {"detail": "Provide a list of project IDs in 'order' key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for position, project_id in enumerate(ids):
            Project.objects.filter(pk=project_id).update(order=position)
        return Response({"detail": "Order updated successfully."})