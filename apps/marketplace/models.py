from django.conf import settings
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("character",   "Character"),
        ("environment", "Environment"),
        ("prop",        "Props and Weapons"),
        ("texture",     "Texture Pack"),
        ("vehicle",     "Vehicle"),
    ]

    title          = models.CharField(max_length=200)
    category       = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES)
    description    = models.TextField()
    price          = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Fill only if the product is on sale")
    rating         = models.PositiveSmallIntegerField(default=5)
    reviews        = models.PositiveIntegerField(default=0)
    downloads      = models.PositiveIntegerField(default=0)
    image          = models.ImageField(
        upload_to="marketplace/", null=True, blank=True)
    icon           = models.CharField(max_length=100, default="fa-solid fa-cube")
    featured       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    date_added     = models.DateField(auto_now_add=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ["-featured", "-created_at"]
        verbose_name        = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    @property
    def is_free(self):
        return self.price == 0

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > 0:
            return int((1 - self.price / self.original_price) * 100)
        return 0


class ProductBadge(models.Model):
    BADGE_CHOICES = [
        ("new",  "New"),
        ("hot",  "Hot"),
        ("sale", "Sale"),
        ("free", "Free"),
    ]
    product = models.ForeignKey(
        Product, related_name="badges", on_delete=models.CASCADE)
    name    = models.CharField(max_length=20, choices=BADGE_CHOICES)

    class Meta:
        unique_together = ["product", "name"]

    def __str__(self):
        return "{} -- {}".format(self.product.title, self.name)


class ProductSoftware(models.Model):
    product = models.ForeignKey(
        Product, related_name="software", on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)

    class Meta:
        unique_together = ["product", "name"]

    def __str__(self):
        return "{} -- {}".format(self.product.title, self.name)


class ProductFormat(models.Model):
    product = models.ForeignKey(
        Product, related_name="formats", on_delete=models.CASCADE)
    name    = models.CharField(max_length=50)

    class Meta:
        unique_together = ["product", "name"]

    def __str__(self):
        return "{} -- {}".format(self.product.title, self.name)


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending",   "Pending"),
        ("completed", "Completed"),
        ("failed",    "Failed"),
        ("refunded",  "Refunded"),
    ]

    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    product     = models.ForeignKey(
        Product,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
    )
    email       = models.EmailField(help_text="Buyer email for receipt")
    full_name   = models.CharField(max_length=200)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    status      = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_ref = models.CharField(
        max_length=200, blank=True,
        help_text="Store Razorpay or Stripe payment ID here")
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ["-created_at"]
        verbose_name        = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return "Order #{} -- {} -- {}".format(
            self.pk, self.product, self.status)