from django.db import models


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("environment", "Environment"),
        ("character",   "Character"),
        ("prop",        "Props and Assets"),
    ]
    GRADIENT_CHOICES = [
        ("env-gradient",  "Environment Gradient"),
        ("char-gradient", "Character Gradient"),
        ("prop-gradient", "Prop Gradient"),
    ]

    title       = models.CharField(max_length=200)
    category    = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="environment")
    description = models.TextField()
    image       = models.ImageField(
        upload_to="portfolio/", null=True, blank=True)
    icon        = models.CharField(
        max_length=100, default="fa-solid fa-cube",
        help_text="Font Awesome class e.g. fa-solid fa-mountain-sun")
    gradient    = models.CharField(
        max_length=50, choices=GRADIENT_CHOICES, default="env-gradient")
    order       = models.PositiveIntegerField(
        default=0, help_text="Lower number appears first")
    is_visible  = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ["order", "-created_at"]
        verbose_name        = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class ProjectTool(models.Model):
    """
    Each tool used in a project is stored as a separate row.
    This allows clean filtering and avoids comma-separated strings.
    """
    project = models.ForeignKey(
        Project, related_name="tools", on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)

    class Meta:
        unique_together = ["project", "name"]

    def __str__(self):
        return "{} -- {}".format(self.project.title, self.name)