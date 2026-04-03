from rest_framework import serializers

from .models import Project, ProjectTool


class ProjectToolSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProjectTool
        fields = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    tools       = ProjectToolSerializer(many=True, read_only=True)
    tools_input = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False,
        help_text="List of tool names e.g. ['Blender', 'ZBrush']",
    )
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Project
        fields = [
            "id", "title", "category", "description",
            "image", "image_url", "icon", "gradient",
            "order", "is_visible",
            "tools", "tools_input",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _save_tools(self, project, tools_list):
        for name in tools_list:
            name = name.strip()
            if name:
                ProjectTool.objects.get_or_create(project=project, name=name)

    # ------------------------------------------------------------------
    # Create / Update
    # ------------------------------------------------------------------
    def create(self, validated_data):
        tools_data = validated_data.pop("tools_input", [])
        project    = Project.objects.create(**validated_data)
        self._save_tools(project, tools_data)
        return project

    def update(self, instance, validated_data):
        tools_data = validated_data.pop("tools_input", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tools_data is not None:
            instance.tools.all().delete()
            self._save_tools(instance, tools_data)
        return instance