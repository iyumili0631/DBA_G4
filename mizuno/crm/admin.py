from django.contrib import admin
from .models import Customer, CustomerOrder, SalesTask, RFMAnalysis, MarketingMetrics

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_purchase_date', 'avg_purchase_interval', 'avg_purchase_value', 'avg_customer_years', 'lifetime_value']
    fields = ['customer_ID', 'name', 'last_purchase_date', 'avg_purchase_interval', 'avg_purchase_value', 'avg_customer_years', 'lifetime_value']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerOrder)
admin.site.register(SalesTask)
admin.site.register(RFMAnalysis)
admin.site.register(MarketingMetrics)

