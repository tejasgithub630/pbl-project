from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
   
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_stock_level = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def current_stock(self):
        return self.stock_set.first().quantity if self.stock_set.exists() else 0

    @property
    def is_low_stock(self):
        return self.current_stock <= self.min_stock_level

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)
        # Update stock
        stock = Stock.objects.get(product=self.product)
        stock.quantity -= self.quantity
        stock.save()

    def __str__(self):
        return f"Sale of {self.quantity} {self.product.name}"

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)
        # Update stock
        stock, created = Stock.objects.get_or_create(product=self.product)
        stock.quantity += self.quantity
        stock.save()

    def __str__(self):
        return f"Purchase of {self.quantity} {self.product.name}"
