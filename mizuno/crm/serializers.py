from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'last_purchase_date', 'avg_purchase_interval', 'avg_purchase_value', 'avg_customer_years', 'lifetime_value']
                  

class CustomerOrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.name')
    order_product = serializers.CharField(source='order_product.product_name')

    class Meta:
        model = CustomerOrder
        fields = '__all__'


        
class SalesTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesTask
        fields = '__all__'

class RFMAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFMAnalysis
        fields = '__all__'

class MarketingMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingMetrics
        fields = '__all__'
