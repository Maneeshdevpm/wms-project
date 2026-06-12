from django.contrib import admin
from .models import Product
from .models import Product, StockTransaction

admin.site.register(Product)
admin.site.register(StockTransaction)