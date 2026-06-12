from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return self.name


class StockTransaction(models.Model):

    TRANSACTION_IN = "IN"
    TRANSACTION_OUT = "OUT"

    TRANSACTION_CHOICES = [
        (TRANSACTION_IN, "Stock In"),
        (TRANSACTION_OUT, "Stock Out"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        # ONLY run logic when creating new transaction
        if not self.pk:

            if self.transaction_type == self.TRANSACTION_IN:
                self.product.quantity += self.quantity

            elif self.transaction_type == self.TRANSACTION_OUT:

                # SAFETY CHECK (VERY IMPORTANT)
                if self.product.quantity < self.quantity:
                    raise ValueError("Not enough stock!")

                self.product.quantity -= self.quantity

            self.product.save()

        super().save(*args, **kwargs)