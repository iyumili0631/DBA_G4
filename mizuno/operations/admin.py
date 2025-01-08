from django.contrib import admin
from .models import BOM, ProductionOrder, Task, Product, Material, ProductRestock, MaterialRestock

# Register your models here.
admin.site.register(BOM)
admin.site.register(ProductionOrder)
admin.site.register(Task)
admin.site.register(Product)
admin.site.register(Material)
admin.site.register(ProductRestock)
admin.site.register(MaterialRestock)