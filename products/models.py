from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)  # nechta borligini hisoblash

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        return self.quantity > 0


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # umumiy narxni hisoblaydi
        if not self.total_price:
            self.total_price = self.product.price * self.quantity

        # mahsulot sonini kamaytiradi
        if self.pk is None:  # faqat yangi buyurtmada
            if self.product.quantity >= self.quantity:
                self.product.quantity -= self.quantity
                self.product.save()
            else:
                raise ValueError("Mahsulot yetarli emas!")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Buyurtma: {self.product.name} ({self.quantity} dona)"
