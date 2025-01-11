from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerOrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.name')


    class Meta:
        model = CustomerOrder
        fields = '__all__'


        
class SalesTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesTask
        fields = '__all__'

class RFMAnalysisSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.name')

    class Meta:
        model = RFMAnalysis
        fields = '__all__'

class MarketingMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingMetrics
        fields = '__all__'
