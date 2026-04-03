from rest_framework import serializers

from .models import Order, Product, ProductBadge, ProductFormat, ProductSoftware


class ProductBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductBadge
        fields = ["id", "name"]


class ProductSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductSoftware
        fields = ["id", "name"]


class ProductFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductFormat
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    badges   = ProductBadgeSerializer(many=True, read_only=True)
    software = ProductSoftwareSerializer(many=True, read_only=True)
    formats  = ProductFormatSerializer(many=True, read_only=True)

    badges_input   = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False)
    software_input = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False)
    formats_input  = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False)

    image_url        = serializers.SerializerMethodField(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    is_free          = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Product
        fields = [
            "id", "title", "category", "description",
            "price", "original_price", "discount_percent", "is_free",
            "rating", "reviews", "downloads",
            "image", "image_url", "icon",
            "badges",   "badges_input",
            "software", "software_input",
            "formats",  "formats_input",
            "featured", "is_active", "date_added",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "date_added", "created_at", "updated_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def _save_related(self, product, badges, software, formats):
        if badges is not None:
            product.badges.all().delete()
            for b in badges:
                b = b.strip().lower()
                if b:
                    ProductBadge.objects.get_or_create(product=product, name=b)
        if software is not None:
            product.software.all().delete()
            for s in software:
                s = s.strip()
                if s:
                    ProductSoftware.objects.get_or_create(product=product, name=s)
        if formats is not None:
            product.formats.all().delete()
            for f in formats:
                f = f.strip().lower()
                if f:
                    ProductFormat.objects.get_or_create(product=product, name=f)

    def create(self, validated_data):
        badges   = validated_data.pop("badges_input",   None)
        software = validated_data.pop("software_input", None)
        formats  = validated_data.pop("formats_input",  None)
        product  = Product.objects.create(**validated_data)
        self._save_related(product, badges, software, formats)
        return product

    def update(self, instance, validated_data):
        badges   = validated_data.pop("badges_input",   None)
        software = validated_data.pop("software_input", None)
        formats  = validated_data.pop("formats_input",  None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._save_related(instance, badges, software, formats)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source="product.title", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10, decimal_places=2,
        read_only=True,
    )

    class Meta:
        model  = Order
        fields = [
            "id", "user", "product", "product_title", "product_price",
            "email", "full_name", "amount", "status",
            "payment_ref", "notes", "created_at",
        ]
        read_only_fields = ["id", "user", "status", "amount", "created_at"]