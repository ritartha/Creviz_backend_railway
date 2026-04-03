from django.db import models


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ("unread",   "Unread"),
        ("read",     "Read"),
        ("replied",  "Replied"),
        ("archived", "Archived"),
    ]

    full_name  = models.CharField(max_length=200)
    email      = models.EmailField()
    subject    = models.CharField(max_length=300)
    message    = models.TextField()
    status     = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="unread")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering            = ["-created_at"]
        verbose_name        = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return "{} -- {}".format(self.full_name, self.subject)