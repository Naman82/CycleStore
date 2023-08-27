from django.contrib import admin
from .models import Product,Category,Order,ReturnOrder
# Register your models here.
admin.site.register([Product,Category,Order,ReturnOrder])
