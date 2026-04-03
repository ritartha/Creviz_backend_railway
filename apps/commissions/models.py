from django.db import models


class Commission(models.Model):
    STATUS_CHOICES = [
        ("new",         "New"),
        ("reviewing",   "Reviewing"),
        ("accepted",    "Accepted"),
        ("in_progress", "In Progress"),
        ("completed",   "Completed"),
        ("rejected",    "Rejected"),
    ]
    TYPE_CHOICES = [
        ("character",   "Character"),
        ("environment", "Environment"),
        ("prop",        "Props and Assets"),
        ("other",       "Other"),
    ]

    full_name       = models.CharField(max_length=200)
    email           = models.EmailField()
    commission_type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default="character")
    budget          = models.CharField(
        max_length=100, help_text="e.g. 5000 to 10000")
    deadline        = models.DateField(null=True, blank=True)
    description     = models.TextField()
    reference_image = models.ImageField(
        upload_to="commissions/refs/", null=True, blank=True)
    status          = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new")
    admin_notes     = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ["-created_at"]
        verbose_name        = "Commission"
        verbose_name_plural = "Commissions"

    def __str__(self):
        return "{} -- {} -- {}".format(
            self.full_name, self.commission_type, self.status)